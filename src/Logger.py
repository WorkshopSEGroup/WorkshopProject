import logging


def logger(f, name=None):
    """
    save each function call and it's arguments on the event log
    :param f: the function
    :param name: the name of the called function
    :return: call to the function with its arguments
    """
    try:
        if logger.fhwr:  # if logger.fhwr (the file "EventLog.log") is defined and open
            pass
    except:
        # else open it
        logger.fhwr = open("EventLog.log", "w")
    if name is None:  # name = the name of the called function
        name = f.__qualname__
#
    def wrapped(*args, **kwargs):
        try:
            args_str = ''
            first_index = 0
            for arg in range(first_index, len(args)):
                args_str += ", " + str(arg)
            logger.fhwr.write("The function " + str(name) + " was called\n"
            # -------------------- the two lines (maybe the upper one can cause errors) ----------------
                              + "arguments: " + args_str + "\n\n")
                              # + "arguments: " + str(args) + "\n\n")
            #                   + "arguments: " + str(args) + str(kwargs) + "\n\n")
            # ------------------------------------------------------------------------------------------
            result = f(*args, **kwargs)
            return result
        except Exception:
            # print("exception on function: func_name = " + name + ", arguments = " + str(args))
            errorLogger("exception on function: func_name = " + name + ", arguments = " + str(args))
            return f(*args, **kwargs)

    # wrapped.__doc__ = f.__doc__
    return wrapped


def secureLogger(f, name=None):
    """
    replace each argument with the word "string" to protect the security of the users
     (should be changed into secure password)
    :param f: the function
    :param name: the name of the called function
    :return: call to the function with its arguments
    """
    try:
        if logger.fhwr: # if logger.fhwr (the file "EventLog.log") is defined and open
            pass
    except:
        # else open it
        logger.fhwr = open("EventLog.log", "w")
    if name is None:
        name = f.__qualname__ # name = the name of the called function

    def wrapped(*args, **kwargs):
        log_str = "The function " + name + " was called\n" + "arguments: ("
        for arg in args:
            log_str += "string, " # the replacement of one argument in the word "string"
        log_str += (")\n\n")
        logger.fhwr.write(log_str)
        result = f(*args, **kwargs)
        return result

    wrapped.__doc__ = f.__doc__
    return wrapped


def loggerStaticMethod(name, args):
    """
    log the calls to static methods
    :param name: name of the function
    :param args: the arguments that sent on the call to the function
    """
    try:
        if loggerStaticMethod.fhwr: # if the file already open
            pass
    except:
        # else open it
        loggerStaticMethod.fhwr = open("EventLog.log", "w")
        # insert the record into the log
        log_str = "The function " + name + " was called\n" + "arguments: ("
        for arg in args:
            log_str += str(arg)
        log_str += (")\n\n")
        logger.fhwr.write(log_str)


def errorLogger(msg):
    """
    collect all the records of exceptions on the error log
    :param msg: the message which was printed to the screen with the exception
    """
    # Creating a self._logger object with the relevant module name
    logger = logging.getLogger(__name__)
    # Setting the level of self._logger to ERROR (which saves only records of exceptions or worse)
    logger.setLevel(logging.ERROR)
    # Set the message format and file's name
    formatter = logging.Formatter('%(asctime)s >> %(message)s')
    file_handler = logging.FileHandler("ErrorLog.log")
    file_handler.setFormatter(formatter)
    # Creating a self._logger handler object
    logger.addHandler(file_handler)
    # Print the message on the chosen format to the error-log's file
    logger.error(msg)


