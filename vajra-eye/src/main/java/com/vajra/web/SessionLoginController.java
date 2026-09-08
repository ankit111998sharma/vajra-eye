package com.vajra.web;

import com.vajra.entity.AppUser;
import com.vajra.service.AuthService;
import com.vajra.service.CommandCenterService;
import jakarta.servlet.http.HttpSession;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.LinkedHashMap;
import java.util.Map;

@Controller
public class SessionLoginController {

    private final AuthService auth;
    private final CommandCenterService commandCenter;

    public SessionLoginController(AuthService auth, CommandCenterService commandCenter) {
        this.auth = auth;
        this.commandCenter = commandCenter;
    }

    @PostMapping(value = "/login", consumes = MediaType.APPLICATION_FORM_URLENCODED_VALUE)
    public String formLogin(@RequestParam(value = "username", required = false) String username,
                            @RequestParam(value = "password", required = false) String password,
                            HttpSession session) {
        return auth.authenticate(username, password)
                .map(user -> {
                    bind(session, user);
                    return "redirect:/";
                })
                .orElse("redirect:/?error=1");
    }

    @GetMapping("/api/me")
    @ResponseBody
    public Map<String, Object> me(HttpSession session) {
        Map<String, Object> m = new LinkedHashMap<>();
        Object user = session.getAttribute("username");
        if (user == null) {
            m.put("ok", false);
            return m;
        }
        m.put("ok", true);
        m.put("username", user);
        m.put("role", session.getAttribute("role"));
        m.put("displayName", session.getAttribute("displayName"));
        return m;
    }

    @PostMapping("/api/logout")
    @ResponseBody
    public Map<String, Object> logout(HttpSession session) {
        session.invalidate();
        return Map.of("ok", true);
    }

    private void bind(HttpSession session, AppUser user) {
        session.setAttribute("username", user.getUsername());
        session.setAttribute("role", user.getRole());
        session.setAttribute("displayName", user.getDisplayName());
        try {
            commandCenter.audit(user.getUsername(), "LOGIN", user.getRole());
        } catch (Exception ignored) {
        }
    }
}
