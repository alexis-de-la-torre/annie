package dev.adlt.nfl_schedules.influencer.schedule;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import dev.adlt.nfl_schedules.influencer.guard.GuardService;
import lombok.SneakyThrows;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.Map;

@Service
public class ScheduleService {
    @Value("${bucket}")
    String bucket;
    @Value("${instagram-id}")
    String instagramId;

    @Autowired
    GuardService guardService;

    @SneakyThrows
    public void post(String fileName) {
        System.out.println(String.format("Post %s", fileName));

        String imgUrlTemplate = "https://storage.googleapis.com/%s/%s.jpg";
        String imgUrl = String.format(imgUrlTemplate, bucket, fileName.replace(" ", "-").replace("+", "-"));


        WebClient webClient = WebClient.create("https://graph.facebook.com");

        String accessToken = guardService.getAccessToken();

        System.out.println(String.format("imgUrl: %s", imgUrl));
        System.out.println(String.format("instagramId: %s", instagramId));
        System.out.println(String.format("accessToken: %s", accessToken));

        String mediaResponse = webClient.post()
                .uri(uriBuilder -> uriBuilder
                        .path(String.format("/v6.0/%s/media", instagramId))
                        .queryParam("caption", "test test")
                        .queryParam("access_token", accessToken)
                        .queryParam("image_url", imgUrl)
                        .build())
                .exchange()
                .block()
                .bodyToMono(String.class)
                .block();

        System.out.println(String.format("mediaResponse: %s", mediaResponse));

        ObjectMapper objectMapper = new ObjectMapper();

        Map<String, String> map = objectMapper.readValue(mediaResponse, new TypeReference<Map<String, String>>() {});

        String creationId = map.get("id");

        System.out.println(String.format("creationId: %s", creationId));

        String mediaPublishResponse = webClient.post()
        .uri(uriBuilder -> uriBuilder
                .path(String.format("/v6.0/%s/media_publish", instagramId))
                .queryParam("access_token", accessToken)
                .queryParam("creation_id", creationId)
                .build())
        .exchange()
        .block()
        .bodyToMono(String.class)
        .block();

        System.out.println(String.format("mediaResponse: %s", mediaPublishResponse));
    }
}
