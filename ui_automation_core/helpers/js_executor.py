def execute_javascript(self, script, *args):
    """
    Synchronously executes JavaScript in the current window or frame.

    :Args:
     - script: The JavaScript to execute.
     - *args: Any applicable arguments for your JavaScript.
    """
    try:
        value = self.context.driver.execute_script(script, *args)

        self.context.logger.info(f'Successfully executed javascript {script} on the '
                                 f'argument(s) {args if len(args) > 0 else "No args"}')
        if value is not None:
            self.context.logger.info(f'Result : {value}')
        return value
    except Exception as ex:
        self.context.logger.error(f'Unable to execute javascript {script} on the '
                                  f'argument(s) {args if len(args) > 0 else "No args"}.')
        self.context.logger.exception(ex)
        raise Exception('Unable to execute javascript {script} on the '
                        f'argument(s) {args if len(args) > 0 else "No args"}. Error: {ex}')