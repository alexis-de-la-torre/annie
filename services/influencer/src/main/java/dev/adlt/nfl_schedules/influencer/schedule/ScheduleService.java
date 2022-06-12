package dev.adlt.nfl_schedules.influencer.schedule;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import dev.adlt.nfl_schedules.influencer.guard.GuardService;
import lombok.SneakyThrows;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.util.UriBuilder;
import reactor.core.publisher.Mono;

import java.net.URI;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
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

        WebClient imgWebClient = WebClient.create(imgUrl);

        HttpStatus imgStatus = imgWebClient.get()
                .exchangeToMono(response -> Mono.just(response.statusCode()))
                .block();

        if (imgStatus == HttpStatus.NOT_FOUND) {
            System.out.println("No image found, skiping");
            System.out.println(imgUrl);
            return;
        }

        WebClient graphWebClient = WebClient.create("https://graph.facebook.com");

        String accessToken = guardService.getAccessToken();

        System.out.println(String.format("imgUrl: %s", imgUrl));
        System.out.println(String.format("instagramId: %s", instagramId));
        System.out.println(String.format("accessToken: %s", accessToken));

        String mediaResponse = graphWebClient.post()
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

        String mediaPublishResponse = graphWebClient.post()
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

    @SneakyThrows
    public void postUrls(List<String> urls) {
        if (urls.size() == 0) {
            System.out.println("No image found, skiping");
            return;
        }

        WebClient graphWebClient = WebClient.create("https://graph.facebook.com");

        String accessToken = guardService.getAccessToken();

        System.out.println(String.format("instagramId: %s", instagramId));
        System.out.println(String.format("accessToken: %s", accessToken));

        List<String> creationIdAcc = new ArrayList<>();

        for (String url : urls) {
            System.out.println(String.format("imgUrl: %s", url));

            String mediaResponse = graphWebClient.post()
                    .uri(uriBuilder -> uriBuilder
                            .path(String.format("/v6.0/%s/media", instagramId))
                            .queryParam("is_carousel_item", "true")
                            .queryParam("image_url", url)
                            .queryParam("access_token", accessToken)
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

            creationIdAcc.add(creationId);
        }

        String mediaResponse = graphWebClient.post()
                .uri(uriBuilder -> uriBuilder
                        .path(String.format("/v6.0/%s/media", instagramId))
                        .queryParam("caption", "#mlb")
                        .queryParam("media_type", "CAROUSEL")
                        .queryParam("children", String.join(",", creationIdAcc))
                        .queryParam("access_token", accessToken)
                        .build())
                .exchange()
                .block()
                .bodyToMono(String.class)
                .block();

        System.out.println(String.format("carousel mediaResponse: %s", mediaResponse));

        ObjectMapper objectMapper = new ObjectMapper();

        Map<String, String> map = objectMapper.readValue(mediaResponse, new TypeReference<Map<String, String>>() {});

        String carouselCreationId = map.get("id");

        System.out.println(String.format("carouselCreationId: %s", carouselCreationId));

        String mediaPublishResponse = graphWebClient.post()
                .uri(uriBuilder -> uriBuilder
                        .path(String.format("/v6.0/%s/media_publish", instagramId))
                        .queryParam("creation_id", carouselCreationId)
                        .queryParam("access_token", accessToken)
                        .build())
                .exchange()
                .block()
                .bodyToMono(String.class)
                .block();

        System.out.println(String.format("last mediaResponse: %s", mediaPublishResponse));
    }
}
