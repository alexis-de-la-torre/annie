package dev.adlt.nfl_schedules.influencer;

import dev.adlt.nfl_schedules.influencer.guard.GuardService;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.assertEquals;

@SpringBootTest
public class GuardTests {
    @Autowired
    GuardService guardService;

    @Disabled
    @Test
    public void accessToken() {
        String accessToken = guardService.getAccessToken();

        assertEquals("", "");
    }
}
