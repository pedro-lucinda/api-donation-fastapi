from fastapi import APIRouter, Depends, HTTPException

from app.infra.logger.config import logger

from . import schemas
from .dependencies import get_cause_repository
from .repository import CauseRepository

cause_routes = APIRouter(prefix="/causes", tags=["Causes"])


@cause_routes.post("/", response_model=schemas.CauseSchema)
def create_cause(
    cause: schemas.CreateCause,
    cause_repository: CauseRepository = Depends(get_cause_repository),
):
    try:
        new_cause_dict = cause_repository.create_cause(cause)
        logger.info("Cause created successfully: %s", new_cause_dict['id'])
        return schemas.CauseSchema(**new_cause_dict)
    except Exception as e:
        logger.error("An error occurred when creating a cause: %s", e)
        raise HTTPException(status_code=400, detail=str(e)) from e


@cause_routes.put("/{cause_id}/{user_id}", response_model=schemas.CauseSchema)
def update_cause(
    cause_id: int,
    user_id: int,
    cause: schemas.UpdateCause,
    cause_repository: CauseRepository = Depends(get_cause_repository),
):
    """
    Update a cause.

    This route receives a cause_id in the path parameters and an UpdateCause schema in the
    request body, validates them, and uses the CauseRepository to update the cause in the
    database.

    Parameters
    ----------
    cause_id : int
        The ID of the cause to be updated.
    cause : UpdateCause
        The schema representing the cause fields to be updated.
    cause_repository : CauseRepository = Depends(get_cause_repository)
        The instance of CauseRepository used to perform database operations.

    Returns
    -------
    CreateCause
        The schema representing the updated cause.
    """
    try:
        updated_cause = cause_repository.update_cause(cause_id, user_id, cause)
        logger.info("Cause updated successfully: %s", updated_cause.id)
        return updated_cause
    except Exception as e:
        logger.error("An error occurred when updating a cause: %s", e)
        raise HTTPException(status_code=400, detail=str(e)) from e


@cause_routes.get("/{cause_id}", response_model=schemas.CauseSchema)
def get_cause(
    cause_id: int,
    cause_repository: CauseRepository = Depends(get_cause_repository),
):
    """
    Get a cause.

    This route receives a cause_id in the path parameters and uses the CauseRepository to get the
    cause from the database.

    Parameters
    ----------
    cause_id : int
        The ID of the cause to be retrieved.
    cause_repository : CauseRepository = Depends(get_cause_repository)
        The instance of CauseRepository used to perform database operations.

    Returns
    -------
    CreateCause
        The schema representing the retrieved cause.
    """
    try:
        cause = cause_repository.get_cause_by_id(cause_id)
        logger.info("Cause retrieved successfully: %s", cause.id)
        print("CAUSEEEEEEEEEEEE__", cause)
        return cause
    except Exception as e:
        logger.error("An error occurred when retrieving a cause: %s", e)
        raise HTTPException(status_code=400, detail=str(e)) from e


@cause_routes.get("/", response_model=schemas.CausesList)
def list_causes(
    cause_repository: CauseRepository = Depends(get_cause_repository),
):
    """
    List all causes.

    This route uses the CauseRepository to get all causes from the database.

    Parameters
    ----------
    cause_repository : CauseRepository = Depends(get_cause_repository)
        The instance of CauseRepository used to perform database operations.

    Returns
    -------
    ListCauses
        The schema representing the list of causes.
    """
    try:
        causes = cause_repository.list_causes()
        logger.info("Causes retrieved successfully")
        return schemas.CausesList(causes=causes)
    except Exception as e:
        logger.error("An error occurred when retrieving causes: %s", e)
        raise HTTPException(status_code=400, detail=str(e)) from e


@cause_routes.put(
    "/activate/{user_id}/{cause_id}", response_model=schemas.CauseSchema
)
def toogle_active_cause(
    user_id: int,
    cause_id: int,
    cause_repository: CauseRepository = Depends(get_cause_repository),
):
    """
    Activate or deactivate a cause.

    This route receives a cause_id in the path parameters and uses the CauseRepository to
    activate or deactivate the cause in the database.

    Parameters
    ----------
    cause_id : int
        The ID of the cause to be activated or deactivated.
    cause_repository : CauseRepository = Depends(get_cause_repository)
        The instance of CauseRepository used to perform database operations.

    Returns
    -------
    CreateCause
        The schema representing the updated cause.
    """
    try:
        updated_cause = cause_repository.toogle_cause_active(user_id, cause_id)
        logger.info("Cause updated successfully: %s", updated_cause.id)
        return updated_cause
    except Exception as e:
        logger.error("An error occurred when updating a cause: %s", e)
        raise HTTPException(status_code=400, detail=str(e)) from e
