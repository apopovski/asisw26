// @ts-nocheck
/* global require, process, Buffer, module */
const crypto = require("crypto");

const REQUIRED_ENV = [
	"ASISW_EDIT_PASSWORD",
	"GITHUB_TOKEN",
	"GITHUB_OWNER",
	"GITHUB_REPO",
	"GITHUB_BRANCH",
];

const CONTENT_PATH = process.env.GITHUB_CONTENT_PATH || "site-content.json";

const send = (res, status, data) => {
	res.status(status).json(data);
};

const safeEqual = (a, b) => {
	const aBuf = Buffer.from(String(a || ""));
	const bBuf = Buffer.from(String(b || ""));
	if (aBuf.length !== bBuf.length) return false;
	return crypto.timingSafeEqual(aBuf, bBuf);
};

const validatePayload = (payload) => {
	if (!payload || typeof payload !== "object") return false;
	const hasNodes = payload.nodes && typeof payload.nodes === "object";
	const hasEventLists = payload.eventLists && typeof payload.eventLists === "object";
	return hasNodes || hasEventLists;
};

const getPayloadFromRequest = (req) => {
	const raw = req.body;
	if (!raw) return null;
	if (typeof raw === "string") {
		try {
			return JSON.parse(raw);
		} catch {
			return null;
		}
	}
	if (typeof raw === "object") {
		return raw;
	}
	return null;
};

module.exports = async (req, res) => {
	if (req.method === "OPTIONS") {
		res.setHeader("Allow", "POST,OPTIONS");
		return res.status(204).end();
	}

	if (req.method !== "POST") {
		res.setHeader("Allow", "POST,OPTIONS");
		return send(res, 405, { error: "Method not allowed" });
	}

	const missing = REQUIRED_ENV.filter((key) => !process.env[key]);
	if (missing.length) {
		return send(res, 500, {
			error: "Server is not configured",
			missing,
		});
	}

	const passwordFromHeader = req.headers["x-edit-password"];
	if (!safeEqual(passwordFromHeader, process.env.ASISW_EDIT_PASSWORD)) {
		return send(res, 401, { error: "Unauthorized" });
	}

	const payload = getPayloadFromRequest(req);
	if (!validatePayload(payload)) {
		return send(res, 400, {
			error: "Invalid payload",
			hint: "Expected JSON object with nodes and/or eventLists",
		});
	}

	const owner = process.env.GITHUB_OWNER;
	const repo = process.env.GITHUB_REPO;
	const branch = process.env.GITHUB_BRANCH;
	const token = process.env.GITHUB_TOKEN;
	const contentUrl = `https://api.github.com/repos/${owner}/${repo}/contents/${CONTENT_PATH}`;

	try {
		const getRes = await fetch(`${contentUrl}?ref=${encodeURIComponent(branch)}`, {
			headers: {
				Authorization: `Bearer ${token}`,
				Accept: "application/vnd.github+json",
				"User-Agent": "asisw2026-publisher",
			},
		});

		let sha;
		if (getRes.status === 200) {
			const existing = await getRes.json();
			sha = existing.sha;
		} else if (getRes.status !== 404) {
			const details = await getRes.text();
			return send(res, 502, { error: "Failed to read target file", details });
		}

		const content = Buffer.from(`${JSON.stringify(payload, null, 2)}\n`, "utf8").toString("base64");
		const body = {
			message: "chore(content): publish schedule edits",
			content,
			branch,
			sha,
		};

		const putRes = await fetch(contentUrl, {
			method: "PUT",
			headers: {
				Authorization: `Bearer ${token}`,
				Accept: "application/vnd.github+json",
				"Content-Type": "application/json",
				"User-Agent": "asisw2026-publisher",
			},
			body: JSON.stringify(body),
		});

		if (!putRes.ok) {
			const details = await putRes.text();
			return send(res, 502, { error: "Failed to publish content", details });
		}

		return send(res, 200, { ok: true });
	} catch (error) {
		return send(res, 500, {
			error: "Unexpected publish error",
			details: error instanceof Error ? error.message : String(error),
		});
	}
};
