package com.vajra.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.InputStream;
import java.net.URI;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;

final class ModelCache {

    private static final Logger log = LoggerFactory.getLogger(ModelCache.class);

    private ModelCache() {
    }

    static Path dir() {
        Path dir = Path.of(System.getProperty("user.home"), ".vajra-eye", "models");
        try {
            Files.createDirectories(dir);
        } catch (Exception ignored) {
        }
        return dir;
    }

    static Path download(String fileName, String... urls) {
        Path dest = dir().resolve(fileName);
        if (Files.isRegularFile(dest) && fileSize(dest) > 1000) {
            return dest;
        }
        for (String url : urls) {
            try (InputStream in = URI.create(url).toURL().openStream()) {
                Files.copy(in, dest, StandardCopyOption.REPLACE_EXISTING);
                if (fileSize(dest) > 1000) {
                    log.info("Cached model {}", dest.getFileName());
                    return dest;
                }
            } catch (Exception e) {
                log.warn("Download {} failed: {}", url, e.getMessage());
            }
        }
        return Files.isRegularFile(dest) ? dest : null;
    }

    private static long fileSize(Path path) {
        try {
            return Files.size(path);
        } catch (Exception e) {
            return 0;
        }
    }
}
