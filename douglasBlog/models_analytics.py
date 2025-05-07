import uuid

from sqlalchemy.dialects.postgresql import UUID
from douglasBlog import db

class PageView(db.Model):
    __tablename__ = 'page_views'


    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    path = db.Column(db.Text, nullable=False)
    visitor_id = db.Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    occurred_at = db.Column(
        db.DateTime(timezone=True), server_default=db.func.now(), nullable=False
    )


    __tableargs__ = (
        db.Index('ix_pageviews_path_occurred', 'path', 'occurred_at'),
    )

    def __repr__(self):
        return f"<PageView path={self.path!r} at={self.occurred_at}>"
