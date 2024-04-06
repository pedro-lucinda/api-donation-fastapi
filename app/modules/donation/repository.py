from sqlalchemy.orm import Session

from app.infra.db.models import Donation

from .schemas import CreateDonation, UpdateDonation


class DonationRepository:
    """
    Repository for performing database operations related to `Donation` entities.

    Attributes
    ----------
    db : Session
        The SQLAlchemy database session used for database operations.
    """

    def __init__(self, db: Session) -> None:
        """
        Initializes the DonationRepository with the given database session.

        Parameters
        ----------
        db : Session
            The SQLAlchemy session to use for database operations.
        """
        self.db = db

    def create_donation(self, data: CreateDonation):
        """
        Creates a new `Donation` entity in the database.

        Parameters
        ----------
        data : CreateDonation
            The data to use for creating the `Donation` entity.

        Returns
        -------
        Donation
            The newly created `Donation` entity.
        """
        donation = Donation(**data.model_dump())
        self.db.add(donation)
        self.db.commit()
        self.db.refresh(donation)
        return donation

    def update_donation(self, user_id: int, donation_id: int, data: UpdateDonation):
        """
        Updates an existing `Donation` entity in the database.

        Parameters
        ----------
        user_id : int
            The ID of the user associated with the donation.
        donation_id : int
            The ID of the `Donation` entity to update.
        data : UpdateDonation
            The data to use for updating the `Donation` entity.

        Returns
        -------
        Donation
            The updated `Donation` entity.
        """
        # Ensure the donation exists and is associated with the user
        donation = self.db.query(Donation).filter_by(id=donation_id, user_id=user_id).first()

        if not donation:
            raise ValueError("No donation found for this user with the provided ID.")

        for key, value in data.model_dump().items():
            setattr(donation, key, value)

        self.db.commit()
        self.db.refresh(donation)
        return donation

    def get_donation_by_id(self, donation_id: int):
        """
        Retrieves a `Donation` entity from the database by its ID.

        Parameters
        ----------
        donation_id : int
            The ID of the `Donation` entity to retrieve.

        Returns
        -------
        Donation
            The retrieved `Donation` entity.
        """
        return self.db.query(Donation).filter_by(id=donation_id).first()
