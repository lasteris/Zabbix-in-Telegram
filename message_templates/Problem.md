# Template

## Subject

```txt
{{{TRIGGER.SEVERITY}}} Problem: {EVENT.NAME}
```

## Message

```txt
Problem started at: {EVENT.TIME} on {EVENT.DATE}
Host: {HOST.NAME} - IP: {HOST.IP}
Severity: {TRIGGER.SEVERITY}
Operational data: {EVENT.OPDATA}

zbxtg;graphs
zbxtg;itemid:{ITEM.ID1}
zbxtg;title:{HOST.HOST} - {TRIGGER.NAME} - Last 3 hours
zbxtg;graphs_period=10800
zbxtg;graphs_width=800
zbxtg;graphs_height=250
```
