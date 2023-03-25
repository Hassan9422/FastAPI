# specifying the base image of our custome image in current dockerfile

FROM python:3.9.7

# here we are going to tell docker where we wanna run all our next commands from. it's like a cd to a specific directory
# to specify where our commands run from

WORKDIR  /usr/src/app

# below command just copies the requirments.txt file into current directory of our docker container.
# './' shows the current directory.
COPY requirments.txt ./

# we are gonna run this command to install all the required dependencies
RUN pip install -r requirments.txt

# first . means "everything" in current dir of docker container,  and the second . means we wanna copy everything in "current dir"
COPY . .

# final command to run the application inside the docker container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]