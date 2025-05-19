import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (CONF_HOST, EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP)
from custom_components.ga104.ga014 import GA014
from homeassistant.helpers.discovery import load_platform

_LOGGER = logging.getLogger(__name__)

# 配置文件的样式
CONFIG_SCHEMA = vol.Schema(
    {
        "ga014": vol.Schema({vol.Required(CONF_HOST): cv.string})
    }, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    conf = config['ga014']
    hass.data['ga014'] = GA014(hass, conf.get(CONF_HOST))

    def start_zinguo_update_keep_alive(event):
        hass.data['ga014'].start_keep_alive()

    def stop_zinguo_update_keep_alive(event):
        hass.data['ga014'].stop_keep_alive()

    hass.bus.listen_once(EVENT_HOMEASSISTANT_START, start_zinguo_update_keep_alive)
    hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, stop_zinguo_update_keep_alive)

    status = hass.data['ga014']._status
    for key in status.keys():
        load_platform(hass, 'climate', 'ga014', {'id': key, 'name': status[key]['name']}, config)
    return True
