#  Copyright (C) 2016 - Yevgen Muntyan
#  Copyright (C) 2016 - Ignacio Casal Quinteiro
#  Copyright (C) 2016 - Arnavion
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>.
import json

import typer

from gvsbuild.utils.base_project import Project, ProjectType


def list_projects(
    project_type: ProjectType = typer.Option(
        None,
        "--type",
        help="Specify type of projects to show, if not selected show all",
        rich_help_panel="Selection Options",
    ),
    json_: bool = typer.Option(
        False,
        "--json",
        help="Show list in JSON format",
        rich_help_panel="Formatting Options",
    ),
):
    Project.add_all()

    projects = Project.list_projects()
    if project_type:
        projects = [
            project for project in projects if project.type.value == project_type
        ]

    if json_:

        def _get_project_data(project):
            data = {"dependencies": project.dependencies, "type": project.type.value}
            if project.version:
                data["version"] = project.version
            return data

        print(
            json.dumps(
                {project.name: _get_project_data(project) for project in projects},
                indent=4,
                sort_keys=True,
            )
        )
    else:
        for project_type in ProjectType:
            type_projects = [
                project for project in projects if project.type == project_type
            ]
            if type_projects:
                print(f"Available projects with type {project_type}:")
                for project in type_projects:
                    print(f"\t{project.name:<{Project.name_len}} {project.version}")
