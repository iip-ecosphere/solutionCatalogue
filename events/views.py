from typing import Dict, Any

from django.views import generic
from icalendar import Calendar


class EventList(generic.TemplateView):
    template_name = "events/event_list.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        f = open("cal.ics")
        ics = f.read()
        cal = Calendar.from_ical(ics)
        context["events"] = [
            {"summary": e.get("summary"),
             "location": e.get("location"),
             "description": e.get("description"),
             "start": e.get("dtstart").dt,
             "end": e.get("dtend").dt,
             } for e in cal.walk("vevent")
        ]
        return context


class EventDetail(generic.TemplateView):
    template_name = "events/event_list.html"
