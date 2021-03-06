from django.contrib.gis.db import models

#from cdmapp.models import Region, DataPolicyLicence


class StationConfigurationLookupFields(models.Model):

    primary_id = models.CharField(max_length=256)
    record_number = models.IntegerField()

    region = models.IntegerField(null=True, blank=True)
    data_policy_licence = models.IntegerField()
    primary_station_id_scheme = models.IntegerField()
    location_accuracy = models.FloatField()
    location_method = models.TextField(max_length=256)
    location_quality = models.IntegerField()
    height_of_station_above_local_ground = models.FloatField(null=True, blank=True)
    height_of_station_above_sea_level = models.FloatField(null=True, blank=True)
    height_of_station_above_sea_level_accuracy = models.FloatField(null=True, blank=True)
    sea_level_datum = models.FloatField(null=True, blank=True)
    source_id = models.CharField(max_length=256)

    class Meta:
        app_label = 'deliveries_app'
