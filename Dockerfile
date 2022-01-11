#
# MAINTAINER Nj Nafir <github.com/njNafir>
#
# EXPOSE 8000
#
# ADD . /django_
#
# WORKDIR /django_
#
# RUN pip install -r requirements.txt
#
# RUN python manage.py makemigrations
#
# RUN python manage.py migrate
#
# CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

FROM python:3.7-buster
RUN mkdir /home/ascorcase
WORKDIR /home/ascorcase
COPY ./ /home/ascorcase/
RUN pip install -r /home/ascorcase/requirements.txt
EXPOSE 80
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:80"]
