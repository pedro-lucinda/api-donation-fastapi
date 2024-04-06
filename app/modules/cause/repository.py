from sqlalchemy.orm import Session

from app.infra.db.models import Cause, Institute

from .schemas import CauseSchema, CreateCause, UpdateCause


class CauseRepository:
    """
    Repository for performing database operations related to `User` entity.

    Attributes
    ----------
    db : Session
        The SQLAlchemy database session used for database operations.
    """

    def __init__(self, db: Session) -> None:
        """
        Initializes the CauseRepository with the given database session.

        Parameters
        ----------
        db : Session
            The SQLAlchemy session to use for database operations.
        """
        self.db = db

    def list_causes(self):
        """
        List all causes in the database.

        This method retrieves all causes from the database.

        Returns
        -------
        List[Cause]
            A list of all causes retrieved from the database.
        """
        return [
            CauseSchema.model_validate(cause)
            for cause in self.db.query(Cause).all()
        ]

    def create_cause(self, data: CreateCause):
        """
        Create a new cause in the database.

        This method creates a new cause in the database using the data provided in the
        CreateCause schema.

        Parameters
        ----------
        data : CreateCause
            The schema representing the cause to be created.

        Returns
        -------
        CreateCause
            The schema representing the created cause.
        """

        if self.get_cause_by_title(
            title=data.title, institute_id=data.institute_id
        ):
            raise ValueError("Cause already exists")

        if not self.is_user_allowed_by_institute(
            user_id=data.user_id, institute_id=data.institute_id
        ):
            raise ValueError("User not allowed")

        cause = Cause(
            title=data.title,
            description=data.description,
            payment_link=data.payment_link,
            image_links=data.image_links,
            is_active=True,
        )

        institute = (
            self.db.query(Institute)
            .filter(Institute.id == data.institute_id)
            .first()
        )
        cause.institute = institute

        self.db.add(cause)
        self.db.commit()
        self.db.refresh(cause)

        return {
            "id": cause.id,
            "title": cause.title,
            "description": cause.description,
            "payment_link": cause.payment_link,
            "image_links": cause.image_links,
            "institute_id": cause.institute_id,
            "is_active": True,
        }

    def update_cause(self, cause_id: int, user_id: int, data: UpdateCause):
        """
        Update a cause in the database.

        This method updates a cause in the database using the data provided in the
        UpdateCause schema.

        Parameters
        ----------
        data : UpdateCause
            The schema representing the cause to be updated.
        cause_id : str
            The ID of the cause to update.
        institute_id : int
            The ID of the institute to which the cause belongs.

        Returns
        -------
        Cause

        """
        if not self.is_user_allowed(user_id=user_id, cause_id=cause_id):
            raise ValueError("User not allowed")

        cause = self.db.query(Cause).filter(Cause.id == cause_id).first()
        if not cause:
            raise ValueError("Cause not found")

        # Assuming `data` is a Pydantic model, use `dict()` to get a dictionary of the fields
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(cause, key, value)

        self.db.commit()
        self.db.refresh(cause)
        return CauseSchema.model_validate(cause)

    def toogle_cause_active(self, user_id: int, cause_id: str):
        """
        Update a cause in the database.

        This method updates a cause in the database using the data provided in the
        UpdateCause schema.

        Parameters
        ----------
        cause_id : str
            The ID of the cause to update.
        institute_id : int
            The ID of the institute to which the cause belongs.

        Returns
        -------
        Cause

        """
        if not self.is_user_allowed(user_id=user_id, cause_id=cause_id):
            raise ValueError("User not allowed")

        cause = self.db.query(Cause).filter(Cause.id == cause_id).first()
        if not cause:
            raise ValueError("Cause not found")

        cause.is_active = not cause.is_active

        self.db.commit()
        self.db.refresh(cause)
        return CauseSchema.model_validate(cause)

    def get_cause_by_title(self, title: str, institute_id: int):
        """
        Get a cause from the database.

        This method retrieves a cause from the database using the title provided.

        Parameters
        ----------
        title : str
            The title of the cause to retrieve.

        Returns
        -------
        Cause
            The cause retrieved from the database.
        """
        return (
            self.db.query(Cause)
            .filter(Cause.title == title and Cause.institute_id == institute_id)
            .first()
        )

    def get_cause_by_id(self, cause_id: int):
        """
        Get a cause from the database.

        This method retrieves a cause from the database using the cause_id provided.

        Parameters
        ----------
        cause_id : int
            The ID of the cause to retrieve.

        Returns
        -------
        Cause
            The cause retrieved from the database.
        """
        cause = self.db.query(Cause).filter(Cause.id == cause_id).first()
        return CauseSchema.model_validate(cause)

    def is_user_allowed(self, user_id: int, cause_id: int) -> bool:
        """
        Check if a user is allowed to access a cause.

        This method checks if a user is allowed to access a cause by checking if the
        user is an admin of the cause's institute.

        Parameters
        ----------
        user_id : int
            The ID of the user to check.
        cause_id : int
            The ID of the cause to check.

        Returns
        -------
        bool
            True if the user is allowed to access the cause, False otherwise.
        """
        cause = self.db.query(Cause).filter(Cause.id == cause_id).first()
        institute = cause.institute
        return user_id in [admin.id for admin in institute.admins]

    def is_user_allowed_by_institute(
        self, user_id: int, institute_id: int
    ) -> bool:
        """
        Check if a user is allowed to access an institute.

        This method checks if a user is allowed to access an institute by checking if the
        user is an admin of the institute.

        Parameters
        ----------
        user_id : int
            The ID of the user to check.
        institute_id : int
            The ID of the institute to check.

        Returns
        -------
        bool
            True if the user is allowed to access the institute, False otherwise.
        """
        institute = (
            self.db.query(Institute)
            .filter(Institute.id == institute_id)
            .first()
        )
        if not institute:
            raise ValueError("Institute not found")

        return user_id in [admin.id for admin in institute.admins]
