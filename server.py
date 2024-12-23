from aiohttp import web
from aiohttp.web import HTTPNotFound, HTTPConflict
from models import init_orm, close_orm, Session, Ad
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
import json

app = web.Application()

def generate_error(error_cls, message):
    error = error_cls(text=json.dumps({'error': message}), content_type='application/json')
    return error

async def get_ad_by_id(session: AsyncSession, ad_id):
    ad =  await session.get(Ad, ad_id)
    if ad is None:
        print(ad_id)
        raise generate_error(HTTPNotFound, 'ad not found')
    return ad
async def add_ad(session: AsyncSession, ad: Ad):
    session.add(ad)
    try:
        await session.commit()
    except IntegrityError:
        raise generate_error(HTTPConflict, 'ad already exists')

async def orm_context(app: web.Application):
    print('Start')
    await init_orm()
    yield
    await close_orm()
    print('Finish')


@web.middleware
async def session_middleware(request, handler):
    async with Session() as session:
        print('before request')
        request.session = session
        result = await handler(request)
        print('after request ')
        return result

app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)

class AdView(web.View):

    @property
    def ad_id(self):
        return int(self.request.match_info["ad_id"])

    async def get(self):
        ad = await get_ad_by_id(self.request.session, self.ad_id)
        return web.json_response(ad.dict)

    async def post(self):
        json_data = await self.request.json()
        ad = Ad(**json_data)
        await add_ad(self.request.session, ad)
        return web.json_response(ad.id_dict)

    async def patch(self):
        json_data = await self.request.json()
        ad = await get_ad_by_id(self.request.session, self.ad_id)
        for field, value in json_data.items():
            setattr(ad, field, value)
        await add_ad(self.request.session, ad)
        return web.json_response(ad.id_dict)

    async def delete(self):
        ad = await get_ad_by_id(self.request.session, self.ad_id)
        await self.request.session.delete(ad)
        await self.request.session.commit()
        return web.json_response({'status': 'deleted'})

app.add_routes(
    [
        web.get('/ad/{ad_id:[0-9]+}', AdView),
        web.patch('/ad/{ad_id:[0-9]+}', AdView),
        web.delete('/ad/{ad_id:[0-9]+}', AdView),
        web.post('/ad', AdView)
    ]
)

web.run_app(app)