from typing import List, Optional, Dict
from pydantic import BaseModel, ConfigDict, Field


class FRCBaseModel(BaseModel):
    # Converts TBA keys all to snake case for consistency in code
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=lambda s: "".join(
            word.capitalize() if i > 0 else word for i, word in enumerate(s.split("_"))
        ),
    )


class Video(FRCBaseModel):
    key: str
    type: str


class HubScore(FRCBaseModel):
    auto_count: int
    auto_points: int
    endgame_count: int
    endgame_points: int
    shift1_count: int
    shift1_points: int
    shift2_count: int
    shift2_points: int
    shift3_count: int
    shift3_points: int
    shift4_count: int
    shift4_points: int
    teleop_count: int
    teleop_points: int
    total_count: int
    total_points: int
    transition_count: int
    transition_points: int
    uncounted: int


class AllianceScore(FRCBaseModel):
    adjust_points: int
    auto_tower_points: int
    auto_tower_robot1: str
    auto_tower_robot2: str
    auto_tower_robot3: str
    end_game_tower_points: int
    end_game_tower_robot1: str
    end_game_tower_robot2: str
    end_game_tower_robot3: str
    energized_achieved: bool
    foul_points: int
    g206_penalty: bool
    hub_score: HubScore
    major_foul_count: int
    minor_foul_count: int
    penalties: str
    rp: int
    supercharged_achieved: bool
    total_auto_points: int
    total_points: int
    total_teleop_points: int
    total_tower_points: int
    traversal_achieved: bool


class AllianceTeams(FRCBaseModel):
    dq_team_keys: List[str]
    score: int
    surrogate_team_keys: List[str]
    team_keys: List[str]


class ScoreBreakdownContainer(FRCBaseModel):
    blue: AllianceScore
    red: AllianceScore


class AlliancesContainer(FRCBaseModel):
    blue: AllianceTeams
    red: AllianceTeams


class FRCMatch(FRCBaseModel):
    key: str
    comp_level: str
    event_key: str
    match_number: int
    set_number: int
    winning_alliance: str
    actual_time: Optional[int] = None
    post_result_time: Optional[int] = None
    predicted_time: Optional[int] = None
    time: int
    alliances: AlliancesContainer
    score_breakdown: Optional[ScoreBreakdownContainer] = None
    videos: List[Video]

    @property
    def is_completed(self) -> bool:
        return self.post_result_time != None

    @property
    def score_delta(self) -> int:
        """Blue Total Points - Red Total Points"""
        return (
            self.score_breakdown.blue.total_points
            - self.score_breakdown.red.total_points
        )

    @property
    def shift_fuel_counts(self) -> list:
        """Total fuel in Auto, Shift 1, Shift 2, Shift 3, Shift 4, and Endgame respectively"""
        blue = self.score_breakdown.blue.hub_score
        red = self.score_breakdown.red.hub_score

        return [
            (blue.auto_count + red.auto_count),
            (blue.transition_count + red.transition_count),
            (blue.shift1_count + red.shift1_count),
            (blue.shift2_count + red.shift2_count),
            (blue.shift3_count + red.shift3_count),
            (blue.shift4_count + red.shift4_count),
            (blue.endgame_count + red.endgame_count),
        ]
