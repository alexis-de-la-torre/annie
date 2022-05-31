package dev.adlt.nfl_schedules.influencer;

import dev.adlt.nfl_schedules.influencer.schedule.ScheduleService;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
public class ScheduleTests {
    @Autowired
    ScheduleService scheduleService;

    @Disabled
    @Test
    void postSchedule() {
        scheduleService.post("2022-05-26T08:52:13.636097 00:00.jpg");
    }
}
