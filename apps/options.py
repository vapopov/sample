from tornado import options


options.define('PORT', type=str, default='8080', help='Application Port')
options.define('DEBUG', type=bool, default=True, help='Debug mode')
options.define('AUTORELOAD', type=bool, default=False, help='Restart applicaiton when source is modified')

options.parse_command_line()

settings = options.options
