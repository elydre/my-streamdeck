import mod.streamdeck as m_sd
import mod.hardware as m_hw
import mod.pihole as m_ph

import time

key_config = {
    2: {
        "render": {
            "name": "active",
            "refresh_after": 0.9,
            "label": lambda args: f"{time.strftime('%H:%M:%S')}\n{time.strftime('%H:%M:%S', time.gmtime())}",
            "size": 18,
        },
        "action": None
    },
    4: {
        "render": {
            "name": "big",
            "label": {
                "default": "+",
                "pressed": lambda args: f"{args['info']['brightness']}"
            }
        },
        "action": lambda args: m_sd.more_brightness(args)
    },
    5: {
        "render": {
            "name": "active",
            "refresh_after": 1,
            "label":  lambda args: f"{sum(args['info']['l_usage']) / len(args['info']['l_usage']):.3f}%\n{max(args['info']['l_usage']):.2f}%\n{args['info']['crsp']:.3f}%\n{args['info']['mid_lps']:.4f}",
            "size": 15,
        },
        "action": lambda args: m_sd.exit_function(args)
    },
    6: {
        "render": {
            "name": "active",
            "refresh_after": 1,
            "label":  lambda args: f"RAM\n{m_hw.get_memory_usage()}%\n{m_hw.get_memory_usage_go():.2f}Go",
            "size": 15,
        },
        "action": None
    },
    7: {
        "render": {
            "name": "active",
            "refresh_after": 1,
            "label":  lambda args: f"CPU\n{m_hw.get_cpu_temp()}°C\n{m_hw.get_cpu_usage()}%",
            "size": 15,
        },
        "action": None
    },
    8: {
        "render": {
            "name": "active",
            "refresh_after": 30,
            "label": {
                "default": lambda args: m_ph.show_info(),
                "pressed": "request\nsent"
            },
            "size": 15,
        },
        "action": lambda args: m_ph.disable()
    },
    9: {
        "render": {
            "name": "big",
            "label": {
                "default": "-",
                "pressed": lambda args: f"{args['info']['brightness']}"
            }
        },
        "action": lambda args: m_sd.less_brightness(args)
    },
    10: {
        "render": {
            "name": "graph",
            "refresh_after": 1,
            "table": lambda args: m_hw.to_graph(args, args["info"]["l_usage"]),
            "color": 0x66FF66,
        },
        "action": None
    },
    11: {
        "render": {
            "name": "graph",
            "refresh_after": 1,
            "table": lambda args: m_hw.graph_psutil(args, "mem"),
            "color": 0x66FFFF,
        },
        "action": None
    },
    12: {
        "render": {
            "name": "graph",
            "refresh_after": 1,
            "table": lambda args: m_hw.graph_psutil(args, "cpu"),
            "color": 0xFFFF00,
        },
        "action": None
    },
    14: {
        "render": {
            "name": "classic",
            "icon": {
                "default": "linux.png",
                "pressed": "linux.png"
            },
            "label": {
                "default": lambda args: m_hw.get_linux_version(),
                "pressed": "refresh"
            }
        },
        "action": None
    },
}
