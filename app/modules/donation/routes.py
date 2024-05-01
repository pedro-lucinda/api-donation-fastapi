from fastapi import APIRouter, Depends, HTTPException

from app.infra.logger.config import logger
from app.modules.auth.dependecies import get_current_user
from app.modules.user.schemas import User

from . import schemas
from .dependencies import get_donation_repository
from .repository import DonationRepository

donation_router = APIRouter(prefix="/donation", tags=["Donation"])


@donation_router.post("/", response_model=schemas.Donation)
def create_donation(
    donation: schemas.CreateDonation,
    user: User = Depends(get_current_user),
    donation_repository: DonationRepository = Depends(get_donation_repository),
):
    """
    Create a new donation with the given user data.

    Parameters
    ----------
    user : schemas.UserCreate
        The user data for creating a new user.
    donation_repository : DonationRepository
        The user repository dependency.

    Returns
    -------
    schemas.User
        The created user object.

    Raises
    ------
    HTTPException
        If the email is already registered.
    """
    try:
        created_donation = donation_repository.create_donation(
            user_id=user.id,
            data=donation,
        )
        logger.info("Donation created successfully: %s", created_donation.id)
        return created_donation
    except ValueError as e:
        logger.error("Error creating donation: {e}")
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.error("Error creating donation: {e}")
        raise HTTPException(status_code=400, detail=str(e)) from e


@donation_router.put("/{donation_id}", response_model=schemas.Donation)
def update_donation(
    donation_id: int,
    donation: schemas.UpdateDonation,
    user: User = Depends(get_current_user),
    donation_repository: DonationRepository = Depends(get_donation_repository),
):
    """
    Update an existing donation with the given user data.

    Parameters
    ----------
    user_id : int
        The ID of the user associated with the donation.
    donation_id : int
        The ID of the donation to update.
    donation : schemas.UpdateDonation
        The data to use for updating the donation.
    donation_repository : DonationRepository
        The donation repository dependency.

    Returns
    -------
    schemas.Donation
        The updated donation object.

    Raises
    ------
    HTTPException
        If the donation does not exist.
    """
    try:
        updated_donation = donation_repository.update_donation(
            user_id=user.id,
            donation_id=donation_id,
            data=donation,
        )
        logger.info("Donation updated successfully: %s", updated_donation.id)
        return updated_donation

    except ValueError as e:
        logger.error("Error updating donation: %s", e)
        raise HTTPException(status_code=400, detail=str(e)) from e


@donation_router.get("/{donation_id}", response_model=schemas.Donation)
def get_donation_by_id(
    donation_id: int,
    donation_repository: DonationRepository = Depends(get_donation_repository),
):
    """
    Get a donation by its ID.

    Parameters
    ----------
    donation_id : int
        The ID of the donation to retrieve.

    Returns
    -------
    schemas.Donation
        The donation object.

    Raises
    ------
    HTTPException
        If the donation does not exist.
    """
    donation = donation_repository.get_donation_by_id(donation_id)
    if not donation:
        logger.error("Donation not found: %s", {donation_id})
        raise HTTPException(status_code=404, detail="Donation not found")
    return donation
