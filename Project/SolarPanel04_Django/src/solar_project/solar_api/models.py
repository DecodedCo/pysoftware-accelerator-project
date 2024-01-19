from django.db import models

class SolarResult(models.Model):
    resultid = models.AutoField(primary_key=True)
    arraytype = models.IntegerField() #models.CharField(max_length=255)
    moduletype = models.IntegerField() #models.CharField(max_length=255)
    lat = models.FloatField()
    lng = models.FloatField()
    area = models.FloatField()
    systemcapacity = models.FloatField()
    tiltangle = models.FloatField()
    azimuthangle = models.FloatField()
    systemlosses = models.FloatField()


    def __str__(self):
        return self.data

from rest_framework import serializers

class SolarResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolarResult
        fields = '__all__'
