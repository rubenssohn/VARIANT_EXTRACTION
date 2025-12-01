'''
VARIANT_EXTRACTION — A Python package and CLI tool to extract and visualize process behaviors from complex event data.
Copyright (C) 2023  Christoffer Rubensson

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Website: https://hu-berlin.de/rubensson
E-Mail: {firstname.lastname}@hu-berlin.de
'''

from .cm_orchestrator import enhance_log_for_concise_model, discover_concise_model
from .visualization.concisemodelbuilder import build_concise_dfg
from .evaluation.evaluation import generate_evaluation_statistics_df

__all__ = [
    "enhance_log_for_concise_model",
    "discover_concise_model",
    "build_concise_dfg",
    "generate_evaluation_statistics_df",
]