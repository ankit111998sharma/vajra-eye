package com.vajra.service;

import com.vajra.entity.AppUser;
import org.springframework.stereotype.Service;

import java.util.Locale;
import java.util.Optional;

@Service
public class AuthService {

    private final VajraDbService db;

    public AuthService(VajraDbService db) {
        this.db = db;
    }

    public Optional<AppUser> authenticate(String rawUser, String rawPass) {
        String username = rawUser == null ? "" : rawUser.trim();
        String password = rawPass == null ? "" : rawPass;
        if (username.isEmpty() || password.isEmpty()) {
            return Optional.empty();
        }
        try {
            Optional<AppUser> fromDb = db.login(username, password);
            if (fromDb.isPresent()) {
                return fromDb;
            }
        } catch (Exception ignored) {
            // fall through to built-in lab accounts
        }
        return builtin(username, password);
    }

    private Optional<AppUser> builtin(String username, String password) {
        String u = username.toLowerCase(Locale.ROOT);
        String role = null;
        if ("localhost".equals(u) && "root".equals(password)) {
            role = "ADMIN";
        } else if ("root".equals(u) && "root".equals(password)) {
            role = "ADMIN";
        } else if ("admin".equals(u) && ("vajra".equals(password) || "root".equals(password) || "admin".equals(password))) {
            role = "ADMIN";
        } else if ("operator".equals(u) && "vajra".equals(password)) {
            role = "FIELD_USER";
        } else if ("cmd".equals(u) && "vajra".equals(password)) {
            role = "CMD_OFFICER";
        }
        if (role == null) {
            return Optional.empty();
        }
        AppUser user = new AppUser();
        user.setUsername(u);
        user.setPassword(password);
        user.setRole(role);
        user.setDisplayName(u);
        return Optional.of(user);
    }
}
