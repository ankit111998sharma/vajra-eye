package com.vajra.service;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;

/**
 * Weapons treated as a threat to living humans.
 * Stock COCO on this webcam: knife, scissors, baseball bat, fork.
 */
public final class WeaponCatalog {

    public static final String SEVERITY_LETHAL = "LETHAL";

    private WeaponCatalog() {
    }

    private static final Set<String> COCO_HUMAN_HARM = Set.of(
            "knife",
            "scissors",
            "baseball bat",
            "fork"
    );

    private static final Map<String, String> COCO_ID = Map.of(
            "34", "baseball bat",
            "42", "fork",
            "43", "knife",
            "76", "scissors"
    );

    private static final Set<String> TRAINED_FIREARMS = Set.of(
            "gun", "pistol", "handgun", "revolver", "rifle", "shotgun",
            "firearm", "assault rifle", "sniper", "machine gun"
    );

    private static final Set<String> TRAINED_EXPLOSIVES = Set.of(
            "grenade", "explosive", "bomb", "rocket", "mine"
    );

    private static final Set<String> TRAINED_EDGED = Set.of(
            "dagger", "machete", "sword", "axe", "blade"
    );

    public static boolean isHumanHarmingWeapon(String className) {
        return lookup(className) != null;
    }

    public static String lookup(String className) {
        if (className == null || className.isBlank()) {
            return null;
        }
        String n = className.toLowerCase(Locale.ROOT).trim();
        int colon = n.indexOf(':');
        if (colon > 0) {
            n = n.substring(colon + 1).trim();
        }
        if (COCO_ID.containsKey(n)) {
            return COCO_ID.get(n);
        }
        if (n.contains("scissor")) {
            return "scissors";
        }
        if (n.contains("baseball bat") || n.equals("bat")) {
            return "baseball bat";
        }
        if (n.contains("knife")) {
            return "knife";
        }
        if (n.equals("fork") || n.endsWith(" fork")) {
            return "fork";
        }
        for (String s : TRAINED_FIREARMS) {
            if (n.equals(s) || n.contains(s)) {
                return s;
            }
        }
        for (String s : TRAINED_EXPLOSIVES) {
            if (n.contains(s)) {
                return s;
            }
        }
        for (String s : TRAINED_EDGED) {
            if (n.contains(s)) {
                return s;
            }
        }
        if (COCO_HUMAN_HARM.contains(n)) {
            return n;
        }
        return null;
    }

    public static boolean shouldAlert(String className, double probability, double configuredMin) {
        if (!isHumanHarmingWeapon(className)) {
            return false;
        }
        double floor = Math.min(Math.max(configuredMin, 0.12), 0.22);
        return probability >= floor;
    }

    public static List<Map<String, String>> listing() {
        List<Map<String, String>> rows = new ArrayList<>();
        add(rows, "person", "Body", "No alert", "Labeled on this camera", "NONE");
        add(rows, "face", "Body", "No alert", "Labeled on this camera", "NONE");
        add(rows, "hand", "Body", "No alert", "Labeled on this camera", "NONE");
        add(rows, "knife", "Edged", "Yes — alert", "Labeled on this camera", SEVERITY_LETHAL);
        add(rows, "scissors", "Edged", "Yes — alert", "Labeled on this camera", SEVERITY_LETHAL);
        add(rows, "fork", "Edged", "Yes — alert", "Labeled on this camera", SEVERITY_LETHAL);
        add(rows, "baseball bat", "Blunt", "Yes — alert", "Labeled on this camera", SEVERITY_LETHAL);
        add(rows, "gun / pistol / rifle", "Firearm", "Yes — alert", "Needs weapon ONNX", SEVERITY_LETHAL);
        add(rows, "cell phone / bottle / chair", "Object", "No alert", "Labeled if COCO sees it", "NONE");
        return rows;
    }

    private static void add(List<Map<String, String>> rows, String name, String kind, String alert, String avail,
                            String severity) {
        Map<String, String> m = new LinkedHashMap<>();
        m.put("weapon", name);
        m.put("kind", kind);
        m.put("alertIfDetected", alert);
        m.put("availability", avail);
        m.put("severity", severity);
        rows.add(m);
    }
}
