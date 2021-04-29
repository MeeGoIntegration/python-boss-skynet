from RuoteAMQP.participant import Participant
from .Control import WorkItemCtrl
import types

class ExoParticipant(Participant):
    """
    This class runs the normal participant handling code.
    In order to support some sophisticated Ruote usage it writes a closure
    into the ParticipantHandler namespace called send_to_engine()
    This closure invokes *this* objects send_to_engine() method and
    uses that to call the super write_to_engine()
    """
    def __init__(self, handler=None, *args, **kwargs):
        super(ExoParticipant, self).__init__(*args, **kwargs)
        self.handler = handler
        # Write a closure into the ParticipantHandler namespace
        self.handler.send_to_engine = types.MethodType(
                lambda orig_obj, wi: self.send_to_engine(wi),
                self.handler)

    # This is called from self.consumer (our ConsumerThread)
    def consume(self, workitem):
        """Workitem consumer.

        This method calls the ParticipantHandler.handle_wi() method.

        It also handles the following common tasks:

          * If workitem.fields.debug_dump or workitem.params.debug_dump is
            defined, workitem is dumped to participant log

        """
        if workitem.fields.debug_trace:
            self.handler.log.info(workitem_summary(workitem))
        if workitem.fields.debug_dump or workitem.params.debug_dump:
            self.handler.log.info(workitem.dump())
        self.handler.handle_wi(workitem)

    # This is called from the main thread and should be fast
    def cancel(self, workitem):
        """Workitem cancel.

        This method calls the ParticipantHandler.handle_wi_control() method.
        """
        self.handler.handle_wi_control(WorkItemCtrl("cancel"))

    # This is called from the main thread to clean up.
    def stop(self, workitem):
        """Workitem cancel.

        This method calls the
        ParticipantHandler.handle_lifecycle_control() method.
        """
        self.handler.handle_lifecycle_control(WorkItemCtrl("stop"))

    def send_to_engine(self, witem):
        self.reply_to_engine(workitem=witem)
