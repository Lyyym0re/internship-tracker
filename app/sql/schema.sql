CREATE TABLE applications(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    company TEXT NOT NULL,
    position TEXT NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'applied',
    CHECK (status IN ('applied', 'interview', 'offer', 'rejected'))
)

