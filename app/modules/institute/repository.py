from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.infra.db.models import Institute, User
from app.modules.user.schemas import User as UserSchema

from .schemas import (
    AddAdmin,
    AdminsList,
    CreateInstitute,
    InstituteSchema,
    UpdateInstitute,
)


class InstituteRepository:
    """
    Repository for performing database operations related to `User` entity.

    Attributes
    ----------
    db : Session
        The SQLAlchemy database session used for database operations.
    """

    def __init__(self, db: Session) -> None:
        """
        Initializes the InstituteRepository with the given database session.

        Parameters
        ----------
        db : Session
            The SQLAlchemy session to use for database operations.
        """
        self.db = db

    def create_institute(
        self, institute_data: CreateInstitute
    ) -> InstituteSchema:
        """
        Create a new institute in the database.

        Parameters
        ----------
        institute_data : CreateInstitute
            The schema representing the institute to be created.

        Returns
        -------
        InstituteSchema
            The schema representing the created institute.
        """
        user = (
            self.db.query(User)
            .filter(User.id == institute_data.user_id)
            .first()
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db_institute = Institute(
            name=institute_data.name,
            email=institute_data.email,
            cnpj=institute_data.cnpj,
            is_active=institute_data.is_active,
        )

        db_institute.admins.append(user)

        self.db.add(db_institute)
        self.db.commit()
        self.db.refresh(db_institute)

        # Assuming InstituteSchema is a Pydantic model with these fields
        return InstituteSchema(
            id=db_institute.id,
            name=db_institute.name,
            email=db_institute.email,
            cnpj=db_institute.cnpj,
            is_active=db_institute.is_active,
        )

    def update_institute(
        self, institute_id: int, user_id: int, data: UpdateInstitute
    ) -> Institute:
        """
        Update an institute in the database.

        This method updates an institute in the database using the given institute_id and
        UpdateInstitute schema.

        Parameters
        ----------
        institute_id : int
            The ID of the institute to be updated.
        institute : UpdateInstitute
            The schema representing the institute fields to be updated.

        Returns
        -------
        Institute
            The model representing the updated institute.
        """
        if not self.is_admin(user_id, institute_id):
            raise HTTPException(
                status_code=403, detail="User is not an admin of the institute"
            )

        updated_institute = (
            self.db.query(Institute)
            .filter(Institute.id == institute_id)
            .first()
        )
        if not updated_institute:
            raise HTTPException(status_code=404, detail="Institute not found")

        # Update the fields from the schema
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(updated_institute, key, value)

        self.db.commit()
        self.db.refresh(updated_institute)
        return updated_institute

    def add_admin(self, data: AddAdmin) -> list[User]:
        """
        Add an admin to an institute.

        This method adds an admin to an institute in the database using the given AddAdmin schema.

        Parameters
        ----------
        data : AddAdmin
            The schema representing the admin to be added to the institute.

        Returns
        -------
        Institute
            The model representing the updated institute.
        """
        institute = (
            self.db.query(Institute)
            .filter(Institute.id == data.institute_id)
            .first()
        )
        if not institute:
            raise HTTPException("Institute not found")

        user = self.db.query(User).filter(User.id == data.user_id).first()
        if not user:
            raise HTTPException("User not found")

        institute.admins.append(user)
        self.db.commit()
        self.db.refresh(institute)
        return institute

    def is_admin(self, user_id: int, institute_id: int) -> bool:
        """
        Check if a user is an admin of an institute.

        This method checks if a user is an admin of an institute by checking if the user is
        present in the institute's admins list.

        Parameters
        ----------
        user_id : int
            The ID of the user to check.
        institute_id : int
            The ID of the institute to check.

        Returns
        -------
        bool
            True if the user is an admin of the institute, False otherwise.

        """
        admin = (
            self.db.query(User)
            .filter(User.id == user_id, User.institute_id == institute_id)
            .first()
        )
        return admin is not None

    def get_admins(self, institute_id: int, user_id: int):
        """
        Get the list of admins of an institute.

        This method gets the list of admins of an institute by checking if the user is an admin of
        the institute and returning the list of admins.

        Parameters
        ----------
        institute_id : int
            The ID of the institute to get the admins of.
        user_id : int
            The ID of the user making the request.

        Returns
        -------
        AdminsList
            The schema representing the list of admins of the institute.

        Raises
        ------
        HTTPException
            If the user is not an admin of the institute.

        HTTPException
            If the institute is not found.
        """
        if not self.is_admin(user_id, institute_id):
            raise HTTPException(
                status_code=403, detail="User is not an admin of the institute"
            )

        institute = (
            self.db.query(Institute)
            .filter(Institute.id == institute_id)
            .first()
        )

        if not institute or not institute.admins:
            raise HTTPException(status_code=404, detail="Not found")

        admin_schemas = [
            UserSchema.model_validate(admin) for admin in institute.admins
        ]

        return AdminsList(admins=admin_schemas)
