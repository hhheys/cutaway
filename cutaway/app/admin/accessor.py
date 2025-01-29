import hashlib

from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.admin.models import Admin
from app.web.utils import BaseAccessor


class AdminAccessor(BaseAccessor):
    async def create_admin(
        self, login: str, password: str
    ) -> Admin:
        hash_password = hashlib.sha256(
            bytearray(password, encoding="utf-8")
        ).hexdigest()

        admin = Admin(login=login, password=hash_password)

        async_session = async_sessionmaker(
            self.app.store.database.engine, expire_on_commit=True, class_=AsyncSession
        )
        async_session.configure(bind=self.app.store.database.engine)
        async with async_session() as session:
            await session.merge(admin)
            try:
                await session.commit()
            except IntegrityError:
                return None
            else:
                return admin

    async def validate_admin(self, login, password):
        async_session = async_sessionmaker(
            self.app.store.database.engine, expire_on_commit=True, class_=AsyncSession
        )
        async_session.configure(bind=self.app.store.database.engine)
        async with async_session() as session:
            hash_password = hashlib.sha256(
                bytearray(password, encoding="utf-8")
            ).hexdigest()
            res = await session.execute(
                select(Admin).where(
                    and_(
                        Admin.login == login,
                        Admin.password == hash_password,
                    )
                )
            )
            data = res.scalar()
            if data is not None:
                return data
            return False