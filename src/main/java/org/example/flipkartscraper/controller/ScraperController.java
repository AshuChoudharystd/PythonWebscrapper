package org.example.flipkartscraper.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.client.RestTemplate;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

@Controller
public class ScraperController {

    private final String FLASK_API_URL = "http://localhost:5000/"; // Update this if your Flask app is running on a different port

    @GetMapping("/")
    public String index() {
        return "index";
    }

    @PostMapping("/scrape")
    public String scrape(@RequestParam String product, Model model) {
        RestTemplate restTemplate = new RestTemplate();
        byte[] csvData = restTemplate.getForObject(FLASK_API_URL + "?product=" + product, byte[].class);

        try {
            Path tempFile = Files.createTempFile("scraped_data", ".csv");
            Files.write(tempFile, csvData);
            model.addAttribute("csvFile", tempFile.toString());
            model.addAttribute("product", product);
        } catch (IOException e) {
            e.printStackTrace();
            model.addAttribute("error", "Error occurred while processing the data.");
        }

        return "result";
    }
}
