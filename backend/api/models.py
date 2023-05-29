from django.db import models

# Create your models here.
class FmJob(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50, unique=True)
    description=models.CharField(max_length=500)
    dml_ts=models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='fm_job'

class FmAction(models.Model):
    id=models.AutoField(primary_key=True )
    fm_job_id=models.ForeignKey(FmJob ,on_delete=models.CASCADE,db_column='fm_job_id')
    
    seq=models.IntegerField(unique=True)
    action_type=models.CharField(max_length=25)
    action_parms=models.CharField(max_length=30000)
    dml_ts=models.DateTimeField(auto_now=True)
    description=models.CharField(max_length=4000)

    class Meta:
        db_table='fm_action'

class FmJobEvent(models.Model):
    id=models.AutoField(primary_key=True)
    fm_job_id=models.ForeignKey(FmJob ,on_delete=models.CASCADE,db_column='fm_job_id')
    start_tms=models.DateTimeField(auto_now=True)
    end_tms=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=20)
    src_ip=models.CharField(max_length=250)

    class Meta:
        db_table='fm_job_event'

class FmJobActionEvent(models.Model):
    id=models.AutoField(primary_key=True)
    fm_job_event_id=models.ForeignKey(FmJobEvent ,on_delete=models.CASCADE,db_column='fm_job_event_id')
    fm_action_id=models.ForeignKey(FmAction ,on_delete=models.CASCADE,db_column='fm_action_id')
    start_tms=models.DateTimeField(auto_now=True)
    end_tms=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=20)
    resolved_action_parms=models.CharField(null=True)   #review

    class Meta:
        db_table='fm_job_action_event'

