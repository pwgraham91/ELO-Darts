ALTER TABLE game ADD COLUMN score_to_0 SMALLINT NOT NULL DEFAULT 201;
ALTER TABLE game ADD COLUMN double_out BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE game ADD COLUMN rebuttal BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE game ADD COLUMN best_of INT NOT NULL DEFAULT 3;

ALTER TABLE game ALTER COLUMN winner_id DROP NOT NULL;
ALTER TABLE game ALTER COLUMN winner_elo_score DROP NOT NULL;
ALTER TABLE game ALTER COLUMN loser_id DROP NOT NULL;
ALTER TABLE game ALTER COLUMN loser_elo_score DROP NOT NULL;

ALTER TABLE game add COLUMN in_progress_player_1_id BIGINT;
ALTER TABLE game add COLUMN in_progress_player_2_id BIGINT;
ALTER TABLE game ADD CONSTRAINT in_progress_player_1_id_fkey FOREIGN KEY (in_progress_player_1_id) REFERENCES "user"(id) ON DELETE CASCADE;
ALTER TABLE game ADD CONSTRAINT in_progress_player_2_id_fkey FOREIGN KEY (in_progress_player_2_id) REFERENCES "user"(id) ON DELETE CASCADE;

CREATE TABLE round(
	id BIGSERIAL NOT NULL PRIMARY KEY,
	game_id bigint NOT NULL,
	first_throw_player_id bigint,
	round_winner_id bigint
);
ALTER TABLE round ADD CONSTRAINT first_throw_player_id_fkey FOREIGN KEY (first_throw_player_id) REFERENCES "user"(id) ON DELETE CASCADE;
ALTER TABLE round ADD CONSTRAINT round_winner_id_fkey FOREIGN KEY (round_winner_id) REFERENCES "user"(id) ON DELETE CASCADE;

CREATE TABLE throw(
	id BIGSERIAL NOT NULL PRIMARY KEY,
	round_id bigint NOT NULL,
	player_id bigint NOT NULL,
	hit_score INTEGER NOT NULL,
	hit_area INTEGER NOT NULL
);
ALTER TABLE throw ADD CONSTRAINT round_id_fkey FOREIGN KEY (round_id) REFERENCES "round"(id) ON DELETE CASCADE;
ALTER TABLE throw ADD CONSTRAINT player_id_fkey FOREIGN KEY (player_id) REFERENCES "user"(id) ON DELETE CASCADE;
