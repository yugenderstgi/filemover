from django.db import models


# Create your models here.
class FilemoverJob(models.Model):
    """_summary_

    Args:
        models (_type_): _description_
    """

    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500)
    dml_ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "fm_job"


class FilemoverAction(models.Model):
    """_summary_

    Args:
        models (_type_): _description_
    """

    fm_job = models.ForeignKey(FilemoverJob, on_delete=models.PROTECT, db_column="fm_job_id")
    seq = models.IntegerField(unique=True)
    action_type = models.CharField(max_length=25)
    action_parms = models.CharField(max_length=30000)
    dml_ts = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=4000)
    precondition_env = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = "fm_action"


class FilemoverJobEvent(models.Model):
    """_summary_

    Args:
        models (_type_): _description_
    """

    # id = models.AutoField(primary_key=True)
    fm_job = models.ForeignKey(FilemoverJob, on_delete=models.PROTECT, db_column="fm_job_id")
    start_tms = models.DateTimeField(null=True, blank=True)
    end_tms = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20)
    src_ip = models.CharField(max_length=250)

    class Meta:
        db_table = "fm_job_event"


class FilemoverJobActionEvent(models.Model):
    """_summary_

    Args:
        models (_type_): _description_
    """

    fm_job_event = models.ForeignKey(FilemoverJobEvent, on_delete=models.PROTECT, db_column="fm_job_event_id")
    fm_action = models.ForeignKey(FilemoverAction, on_delete=models.PROTECT, db_column="fm_action_id")
    start_tms = models.DateTimeField(null=True, blank=True)
    end_tms = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20)
    resolved_action_parms = models.TextField(null=True)

    class Meta:
        db_table = "fm_job_action_event"
