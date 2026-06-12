from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from typing import List, Optional
from database import get_database
from schemas import StudentCreate, StudentResponse

router = APIRouter(prefix="/students", tags=["Students"])

# 1. CREATE: Insert a single student document
@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(student: StudentCreate, db=Depends(get_database)):
    # Convert our Pydantic data into a raw dictionary for MongoDB
    student_data = student.model_dump()

    # Insert into the "students" collection
    new_student = await db["students"].insert_one(student_data)

    # Fetch the newly created document using its generated id
    created_student = await db["students"].find_one({"_id": new_student.inserted_id})
    return created_student

# 2. READ ALL + FILTER SEARCH: Query operations with sorting and limiting
@router.get("/", response_model=List[StudentResponse])
async def get_students(
    age_filter: Optional[int] = None, 
    limit: int = 10, 
    skip: int = 0, 
    db=Depends(get_database)
):
    query = {}
    # If an age query is passed, use the $gte (Greater than or equal) operator
    if age_filter is not None:
        query = {"age": {"$gte": age_filter}}

    # Use a cursor to find, skip, limit, and sort alphabetically by name (1 = Ascending)
    cursor = db["students"].find(query).skip(skip).limit(limit).sort("name", 1)
    students = await cursor.to_list(length=limit)
    return students

# 3. READ SINGLE: Find a single document by its ObjectId
@router.get("/{id}", response_model=StudentResponse)
async def get_student(id: str, db=Depends(get_database)):
    # Catch format errors early before checking database
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId hex format string")

    student = await db["students"].find_one({"_id": ObjectId(id)})
    if student:
        return student
    raise HTTPException(status_code=404, detail="Student document not found")

# 4. UPDATE: Modify specific fields using the $set operator
@router.put("/{id}", response_model=StudentResponse)
async def update_student(id: str, student: StudentCreate, db=Depends(get_database)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")

    update_data = student.model_dump()

    # Perform the update operation using the $set operator
    update_result = await db["students"].update_one(
        {"_id": ObjectId(id)}, {"$set": update_data}
    )

    if update_result.modified_count == 1 or update_result.matched_count == 1:
        updated_student = await db["students"].find_one({"_id": ObjectId(id)})
        return updated_student

    raise HTTPException(status_code=404, detail="Student not found or no shifts made")

# 5. DELETE: Remove a document from the collection
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(id: str, db=Depends(get_database)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")

    delete_result = await db["students"].delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return None # 204 status demands returning an empty body response

    raise HTTPException(status_code=404, detail="Student document not found")