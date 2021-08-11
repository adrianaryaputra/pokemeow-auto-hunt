from abc import ABC, abstractmethod
from typing import Any, List
import threading



class Publisher(ABC):
    """
    abstract class for observer subject
    """

    def registerSub(self, observer):
        """
        register observer to subject
        """
        pass

    def removeSub(self, observer):
        """
        remove observer from subject
        """
        pass

    def notifySub(self, obj: Any = None):
        """
        notify observers about the event
        """
        pass



class Subscriber(ABC):
    """
    abstract class for subscriber
    """
    def __init__(self, obj=None) -> None:
        self.obj = obj

    @abstractmethod
    def call(self, subject):
        """
        update observer
        """
        pass



class BasicPublisher(Publisher):
    """
    basic publisher object
    """

    def __init__(self) -> None:
        self.observers: List[Subscriber] = []

    def registerSub(self, observer: Subscriber):
        self.observers.append(observer)

    def removeSub(self, observer: Subscriber):
        self.observers.remove(observer)

    def notifySub(self, obj: Any = None):
        for observer in self.observers:
            threading.Thread(target=observer.call, args=(obj,)).start()



class BasicSubscriber(Subscriber):
    """
    basic subscriber object
    """

    def call(self, subject):
        print("{} notified".format(self.__class__.__name__))
        print(subject)



def makeSubscriberFromFn(fn, parent: object = None):
    """
    make subscriber from single input function
    """
    sub = BasicSubscriber()
    sub.parent = parent
    sub.call = fn
    return sub