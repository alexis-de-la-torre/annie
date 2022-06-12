package dev.adlt.nfl_schedules.influencer;

import dev.adlt.nfl_schedules.influencer.schedule.ScheduleService;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.Arrays;
import java.util.List;

@SpringBootTest
public class ScheduleTests {
    @Autowired
    ScheduleService scheduleService;

    @Disabled
    @Test
    void postSchedule() {
        scheduleService.post("2022-05-26T08:52:13.636097 00:00.jpg");
    }

    @Disabled
    @Test
    void postScheduleMulti() {
        List<String> urls = Arrays.asList(
                "https://storage.googleapis.com/nfl-schedules/f332bbe9d7a9420fb8f227168a3f1a76.jpg",
                "https://storage.googleapis.com/nfl-schedules/67c14b8a6f0f4bc08ee3f844fa3b7692.jpg",
                "https://storage.googleapis.com/nfl-schedules/d004b71c77014e4998de707e3826be64.jpg",
                "https://storage.googleapis.com/nfl-schedules/70783e09a1374d0bb31c4d9095955d13.jpg"
        );

        scheduleService.postUrls(urls);
    }
}
