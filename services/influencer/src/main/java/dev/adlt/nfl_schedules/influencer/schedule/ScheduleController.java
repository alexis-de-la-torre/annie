package dev.adlt.nfl_schedules.influencer.schedule;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("schedules")
public class ScheduleController {
    @Autowired
    ScheduleService scheduleService;

    @PostMapping
    public String saveSchedule(@RequestBody ScheduleDto scheduleDto) {
        scheduleService.post(scheduleDto.getDate());
        return scheduleDto.getDate();
    }
}
