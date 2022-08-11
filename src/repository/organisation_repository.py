from typing import Optional

from src.models.organisation import Organisation
from src.repository.base_repository import CRUDBase


class OrganisationRepository(CRUDBase[Organisation]):
    """ CRUD`s subclass for interaction with 'organisations' table """

    def get_by_uid(self, uid: str) -> Optional[Organisation]:
        return self.db.query(Organisation).filter(Organisation.id == uid).first()

    def get_by_name(self, name: str) -> Optional[Organisation]:
        return self.db.query(Organisation).filter(Organisation.organisation == name).first()


organisation_repository = OrganisationRepository(Organisation)
