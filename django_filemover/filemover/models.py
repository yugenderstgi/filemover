from django.db import models


# Create your models here.
class FilemoverJob(models.Model):
    """
    Represents a Filemover job.

    Args:
        name (CharField): The name of the Filemover job.
        description (CharField): A description of the Filemover job.
        dml_ts (DateTimeField): The timestamp when the job was last modified.

    Meta:
        db_table (str): The name of the database table associated with the model.
    """

    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500)
    dml_ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "fm_job"


class FilemoverAction(models.Model):
    """
    Represents an Filemover Action associated with a Filemover job.

    Args:
        fm_job (ForeignKey): The FilemoverJob instance that this action belongs to.
        seq (IntegerField): The sequence number of the action.
        action_type (CharField): The type of the action either Transform or Unzip.
        action_parms (CharField): A String type xml format represent parameters to specific action.
        dml_ts (DateTimeField): The timestamp when the action was last modified.
        description (CharField): A description of the action.
        precondition_env (JSONField): JSON representation of the precondition environment for the action.

    Meta:
        db_table (str): The name of the database table associated with the model.
    """

    fm_job = models.ForeignKey(FilemoverJob, on_delete=models.PROTECT, db_column="fm_job_id")
    seq = models.IntegerField(unique=True)
    action_type = models.CharField(max_length=25)
    action_parms = models.CharField(max_length=30000)
    dml_ts = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=4000)
    precondition_env = models.JSONField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "fm_action"


class FilemoverJobEvent(models.Model):
    """
    Represents an execution of the Filemover job.

    Args:
        fm_job (ForeignKey): The FilemoverJob instance that this action belongs to.
        start_tms (DateTimeField): The timestamp when the Job execution was started.
        end_tms (DateTimeField): The timestamp when the Job execution was ended.
        status (CharField): The status of the Job execution either PASS or  FAILED OR SKIPPED.
        src_ip (CharField): The Source IP address of the Job execution.

    Meta:
        db_table (str): The name of the database table associated with the model.
    """

    fm_job = models.ForeignKey(FilemoverJob, on_delete=models.PROTECT, db_column="fm_job_id")
    start_tms = models.DateTimeField(null=True, blank=True)
    end_tms = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20)
    src_ip = models.CharField(max_length=250)

    class Meta:
        db_table = "fm_job_event"


class FilemoverJobActionEvent(models.Model):
    """
    Represents an execution of the Filemover Action.

    Args:
        fm_job_event (ForeignKey): The FilemoverJobEvent instance that this action belongs to.
        fm_action (ForeignKey): The FilemoverAction instance that this action belongs to.
        start_tms (DateTimeField): The timestamp when the Action execution was started.
        end_tms (DateTimeField): The timestamp when the Action execution was ended.
        status (CharField): The status of the Action execution either PASS or  FAILED OR SKIPPED.
        resolved_action_parms (CharField): A String type xml format represent parameters to specific action after execution.

    Meta:
        db_table (str): The name of the database table associated with the model.
    """

    fm_job_event = models.ForeignKey(FilemoverJobEvent, on_delete=models.PROTECT, db_column="fm_job_event_id")
    fm_action = models.ForeignKey(FilemoverAction, on_delete=models.PROTECT, db_column="fm_action_id")
    start_tms = models.DateTimeField(null=True, blank=True)
    end_tms = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20)
    resolved_action_parms = models.TextField(null=True)

    class Meta:
        db_table = "fm_job_action_event"
