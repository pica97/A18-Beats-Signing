#!/usr/bin/env python3
import argparse
import plistlib
import uuid
from pathlib import Path

NS = uuid.UUID("A1800000-0000-4000-8000-000000000002")

def U(name):
    return str(uuid.uuid5(NS, name)).upper()

def output_ref(action_uuid, output_name):
    return {
        "Value": {
            "OutputUUID": action_uuid,
            "Type": "ActionOutput",
            "OutputName": output_name,
        },
        "WFSerializationType": "WFTextTokenAttachment",
    }

def text_action(name, text):
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.gettext",
        "WFWorkflowActionParameters": {
            "UUID": U(name),
            "WFTextActionText": text,
        },
    }

def set_clipboard(name, text_uuid):
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.setclipboard",
        "WFWorkflowActionParameters": {
            "UUID": U(name),
            "WFInput": output_ref(text_uuid, "Text"),
            "WFLocalOnly": True,
        },
    }

def run_core(name):
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.runworkflow",
        "WFWorkflowActionParameters": {
            "UUID": U(name),
            "WFWorkflowName": "A18 Bridge",
            "WFShowWorkflow": False,
        },
    }

def speak(name, text_uuid):
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.speaktext",
        "WFWorkflowActionParameters": {
            "UUID": U(name),
            "WFInput": output_ref(text_uuid, "Text"),
            "WFSpeakTextWait": True,
            "WFSpeakTextRate": 0.44,
            "WFSpeakTextPitch": 0.95,
            "WFSpeakTextLanguage": "Español (México)",
        },
    }

def conditional_start(name, group, input_uuid, expected):
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.conditional",
        "WFWorkflowActionParameters": {
            "UUID": U(name),
            "WFInput": {
                "Type": "Variable",
                "Variable": output_ref(input_uuid, "Clipboard"),
            },
            "WFControlFlowMode": 0,
            "WFCondition": 4,
            "WFConditionalActionString": expected,
            "GroupingIdentifier": group,
        },
    }

def conditional_end(name, group):
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.conditional",
        "WFWorkflowActionParameters": {
            "UUID": U(name),
            "WFControlFlowMode": 2,
            "GroupingIdentifier": group,
        },
    }

def exit_action(name):
    return {
        "WFWorkflowActionIdentifier": "is.workflow.actions.exit",
        "WFWorkflowActionParameters": {"UUID": U(name)},
    }

def build():
    clip_uuid = U("get-clipboard")
    focus_group = U("focus-group")
    sport_group = U("sport-group")
    pause_text_uuid = U("focus-pause-text")
    focus_voice_uuid = U("focus-voice-text")
    resume_text_uuid = U("focus-resume-text")
    sport_voice_uuid = U("sport-voice-text")

    actions = [
        {
            "WFWorkflowActionIdentifier": "is.workflow.actions.getclipboard",
            "WFWorkflowActionParameters": {"UUID": clip_uuid},
        },

        conditional_start("focus-if", focus_group, clip_uuid, "FOCUS"),
        text_action("focus-pause-text", "PAUSE"),
        set_clipboard("focus-set-pause", pause_text_uuid),
        run_core("focus-run-pause"),
        text_action("focus-voice-text", "Modo focus activo"),
        speak("focus-speak", focus_voice_uuid),
        text_action("focus-resume-text", "RESUME"),
        set_clipboard("focus-set-resume", resume_text_uuid),
        run_core("focus-run-resume"),
        exit_action("focus-exit"),
        conditional_end("focus-end", focus_group),

        conditional_start("sport-if", sport_group, clip_uuid, "DEPORTE"),
        text_action("sport-voice-text", "Modo deporte activo"),
        speak("sport-speak", sport_voice_uuid),
        exit_action("sport-exit"),
        conditional_end("sport-end", sport_group),

        run_core("delegate-core"),
    ]

    return {
        "WFWorkflowMinimumClientVersion": 900,
        "WFWorkflowMinimumClientVersionString": "900",
        "WFWorkflowClientVersion": "2302.0.4",
        "WFWorkflowClientRelease": "2302.0.4",
        "WFWorkflowIcon": {
            "WFWorkflowIconStartColor": 4278190335,
            "WFWorkflowIconGlyphNumber": 61440,
        },
        "WFWorkflowTypes": ["NCWidget"],
        "WFWorkflowInputContentItemClasses": [
            "WFStringContentItem",
            "WFGenericFileContentItem",
        ],
        "WFWorkflowOutputContentItemClasses": [],
        "WFWorkflowImportQuestions": [],
        "WFQuickActionSurfaces": [],
        "WFWorkflowHasOutputFallback": False,
        "WFWorkflowHasShortcutInputVariables": False,
        "WFWorkflowActions": actions,
    }

def validate(shortcut):
    ids = [a["WFWorkflowActionIdentifier"] for a in shortcut["WFWorkflowActions"]]
    required = {
        "is.workflow.actions.getclipboard",
        "is.workflow.actions.conditional",
        "is.workflow.actions.gettext",
        "is.workflow.actions.setclipboard",
        "is.workflow.actions.runworkflow",
        "is.workflow.actions.speaktext",
        "is.workflow.actions.exit",
    }
    missing = required.difference(ids)
    if missing:
        raise SystemExit("missing identifiers: " + repr(sorted(missing)))
    if ids.count("is.workflow.actions.conditional") != 4:
        raise SystemExit("expected exactly 2 IF pairs")
    if ids.count("is.workflow.actions.runworkflow") != 3:
        raise SystemExit("expected 3 Run Shortcut actions")
    if ids.count("is.workflow.actions.speaktext") != 2:
        raise SystemExit("expected 2 Speak Text actions")
    return len(ids)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    shortcut = build()
    count = validate(shortcut)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as f:
        plistlib.dump(shortcut, f, fmt=plistlib.FMT_BINARY, sort_keys=False)
    with out.open("rb") as f:
        reloaded = plistlib.load(f)
    if reloaded["WFWorkflowActions"] != shortcut["WFWorkflowActions"]:
        raise SystemExit("plist round-trip mismatch")
    print("A18_BRIDGE_R2_ACTIONS=" + str(count))
    print("A18_BRIDGE_R2_OUTPUT=" + str(out))

if __name__ == "__main__":
    main()
