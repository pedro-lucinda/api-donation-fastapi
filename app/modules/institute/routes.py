from fastapi import APIRouter, Depends, HTTPException

from app.infra.logger.config import logger
from app.modules.user.schemas import User

from . import schemas
from .dependencies import get_institute_repository
from .repository import InstituteRepository

institute_routes = APIRouter(prefix="/institutes", tags=["Institutes"])


@institute_routes.post("/", response_model=schemas.InstituteSchema)
def create_institute(
    institute: schemas.CreateInstitute,
    institute_repository: InstituteRepository = Depends(get_institute_repository),
):
    """
    Create a new institute in the database.

    This endpoint creates a new institute in the database using the given CreateInstitute schema.

    Parameters
    ----------
    institute : CreateInstitute
        The schema representing the institute to be created.
    institute_repository : InstituteRepository
        The repository for performing database operations related to the institute entity.

    Returns
    -------
    Institute
        The model representing the created institute.
    """
    try:
        new_institute = institute_repository.create_institute(institute)
        logger.info("Institute created successfully %s", new_institute.id)
        return new_institute
    except Exception as e:
        logger.error("Error creating institute %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@institute_routes.put("/{institute_id}/{user_id}", response_model=schemas.InstituteSchema)
def update_institute(
    institute_id: int,
    user_id: int,
    data: schemas.UpdateInstitute,
    institute_repository: InstituteRepository = Depends(get_institute_repository),
) -> schemas.InstituteSchema:
    """
    Update an institute in the database.

    This endpoint updates an institute in the database using the given institute_id and UpdateInstitute schema.

    Parameters
    ----------
    institute_id : int
        The ID of the institute to be updated.
    data : UpdateInstitute
        The schema representing the institute fields to be updated.
    institute_repository : InstituteRepository
        The repository for performing database operations related to the institute entity.

    Returns
    -------
    Institute
        The model representing the updated institute.
    """
    try:
        updated_institute = institute_repository.update_institute(institute_id, user_id, data)
        logger.info("Institute updated successfully %s", updated_institute.id)
        return updated_institute
    except Exception as e:
        logger.error("Error updating institute %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@institute_routes.post("/add-admin", response_model=schemas.InstituteSchema)
def add_admin(
    data: schemas.AddAdmin,
    institute_repository: InstituteRepository = Depends(get_institute_repository),
) -> schemas.InstituteSchema:
    """
    Add an admin to an institute.

    This endpoint adds an admin to an institute using the given AddAdmin schema.

    Parameters
    ----------
    data : AddAdmin
        The schema representing the admin and institute to be added.
    institute_repository : InstituteRepository
        The repository for performing database operations related to the institute entity.

    Returns
    -------
    Institute
        The model representing the updated institute.
    """
    try:
        updated_institute = institute_repository.add_admin(data)
        logger.info("Admin added successfully %s", updated_institute.id)
        return updated_institute
    except Exception as e:
        logger.error("Error adding admin %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@institute_routes.get("/{institute_id}/{user_id}/admins", response_model=schemas.AdminsList)
def get_admins(
    institute_id: int,
    user_id: int,
    institute_repository: InstituteRepository = Depends(get_institute_repository),
) -> list[User]:
    """
    Get the admins of an institute.

    This endpoint retrieves the admins of an institute using the given institute_id.

    Parameters
    ----------
    institute_id : int
        The ID of the institute to get the admins from.
    institute_repository : InstituteRepository
        The repository for performing database operations related to the institute entity.

    Returns
    -------
    list[User]
        The list of users representing the admins of the institute.
    """
    try:
        admins = institute_repository.get_admins(institute_id, user_id)
        logger.info("Admins retrieved successfully")
        return admins
    except Exception as e:
        logger.error("Error retrieving admins %s", e)
        raise HTTPException(status_code=500, detail=str(e)) from e
