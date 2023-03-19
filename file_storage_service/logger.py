import logging
import logging.config

from file_storage_service.settings import Config


LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            "format": "%(levelname)s [%(name)s:%(process)d:%(lineno)d] %(asctime)s %(message)s",
        },
    },
    'handlers': {
        'console': {
            'formatter': "default",
            'class': "logging.StreamHandler",
            'stream': "ext://sys.stdout"
        }
    },
    'loggers': {
        '': {
            'level': Config.log_level,
            'handlers': ['console'],
        },
        'rest': {
            'level': Config.log_level,
            'handlers': ['console'],
            'propagate': False
        },
        'utils': {
            'level': Config.log_level,
            'handlers': ['console'],
            'propagate': False
        }
    }
}

logging.config.dictConfig(LOG_CONFIG)
