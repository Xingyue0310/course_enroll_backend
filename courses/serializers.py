from rest_framework import serializers
from courses.models import Course

class CourseSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField
    # course_name = serializers.CharField(required=True, allow_blank=False, max_length=100)
    # course_location = serializers.CharField(required=True, allow_blank=False, max_length=50)
    # course_content = serializers.CharField(required=True, allow_blank=False, max_length=50)
    # teacher_id = serializers.IntegerField()
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'course_location', 'course_content', 'teacher_id']
        # fields = '__all__'

