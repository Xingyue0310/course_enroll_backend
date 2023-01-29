from urllib import response
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from courses.serializers import CourseSerializer
from courses.models import Course

class UserCourseViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, ) # request.user to get user
    #list all the picked courses
    # 1. http method read -> GET
    # 2. url? /user/courses GET 
    # 3. response return string 
    # 4. user input? (student id)?
    @action(methods=['GET'],detail =False)
    def courses(self, request):
        user = request.user
        # read courses list from database
        enrolled_courses = user.courses.all()
        serializer = CourseSerializer(enrolled_courses, many = True)

        return Response(serializer.data, status.HTTP_200_OK)
    
    # @action(methods=['GET'],detail = False, url_path="course/(?P<course_name>[\w\s]+)")
    # def course(self, request, **kwargs):
    #     course_name = kwargs['course_name']
    #     return Response("Enrolled course %$" % course_name, status.HTTP_200_OK)
    
    @action(methods=["POST"], detail=False, url_path="course/(?P<course_name>[\w\s]+)")     
    def course(self, request, **kwargs):         
        course_name = kwargs['course_name']
        user = request.user
        course = Course.objects.filter(course_name=course_name).first()
        # sanity checks
        if course is None:
            raise APIException('course does not exist')
        if user in course.user.all():
            raise APIException('user has already enrolled the course')
        # add the user to the course
        course.user.add(user)
        return Response({}, status.HTTP_204_NO_CONTENT)
    
    @course.mapping.delete
    def drop_course(self, request, **kwargs):
        course_name = kwargs['course_name']
        user = request.user
        course = Course.objects.filter(course_name=course_name).first()
         # sanity checks
        if course is None:
            raise APIException('course does not exist')
        if user not in course.user.all():
            raise APIException('user has not enrolled this course')
        # delete the user from the course
        course.user.remove(user)
        return Response({}, status.HTTP_204_NO_CONTENT)
# Create your views here.

class CourseViewSet( viewsets.ViewSet):
    @action(methods=['GET'], detail=False, )
    def courses(self, request):
        # TODO: read all courses from db
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

class UserInfoViewSet( viewsets.ViewSet):
    @action(methods=['PUT'],detail=False)
    def phone_number(self, request):
        # when you send form-encoded body data, use request.POST to get params
        phone_number = request.POST.get('phone_number')
        # TODO: connect db to update phone number
        return Response("Updated phone number %s" % phone_number, status.HTTP_204_NO_CONTENT) 



