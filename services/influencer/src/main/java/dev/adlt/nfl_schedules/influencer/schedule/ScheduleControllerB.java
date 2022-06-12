package dev.adlt.nfl_schedules.influencer.schedule;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("api/v1/posts")
public class ScheduleControllerB {
    @Autowired
    ScheduleService scheduleService;

    @PostMapping
    public List<String> saveSchedule(@RequestBody List<String> urls) {
        scheduleService.postUrls(urls);
        return urls;
    }
}
