db = db.getSiblingDB("supplyflow");
db.audit_events.createIndex({ created_at: -1 });
db.audit_events.createIndex({ entity_type: 1, entity_id: 1 });

