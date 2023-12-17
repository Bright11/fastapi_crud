from fastapi import FastAPI, Depends as _depends,status,Response,HTTPException
import schema as _schema, models as _models, database as _database 
from sqlalchemy.orm import Session as _session



app=FastAPI()

_models._database.Base.metadata.create_all(_database.engine)

def get_db():
    db=_database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
# creating blog
@app.post("/blog",status_code=status.HTTP_201_CREATED)
def create(request:_schema.Blog,db: _session=_depends(get_db)):
    new_blog=_models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# getting all blogs
@app.get("/blog")
def allblog(db:_session=_depends(get_db)):
    blogs=db.query(_models.Blog).all()
    return blogs

# getting single data
@app.get('/blog/{id}',status_code=200)
def show(id,response: Response,db:_session=_depends(get_db)):
    blog=db.query(_models.Blog).filter(_models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with this id {id} is not available")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'details': f"Blog with this id {id} is not available"}
    return blog

# deleting data
@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,response: Response,db:_session=_depends(get_db)):
    blog=db.query(_models.Blog).filter(_models.Blog.id==id).delete(synchronize_session=False)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with this id {id} is not available")
    db.commit()
    
    return (f"Blog with this id {id} is deleted")

# updating data
@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request:_schema.Blog,db:_session=_depends(get_db)):
    
    blog=db.query(_models.Blog).filter(_models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} no found")
    blog.title=request.title
    blog.body=request.body
    db.commit()
    return "updated"


