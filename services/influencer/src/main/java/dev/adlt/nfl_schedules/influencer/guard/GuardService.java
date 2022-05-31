package dev.adlt.nfl_schedules.influencer.guard;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

@Service
public class GuardService {
    @Value("${guard-url}")
    String guardUrl;

    public String getAccessToken() {
        WebClient webClient = WebClient.create(guardUrl);

        String accessToken = webClient.get()
                .uri("/get_saved_access_token.php")
                .exchange()
                .block()
                .bodyToMono(String.class)
                .block();

        return accessToken;
    }
}
