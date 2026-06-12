import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

from launch.substitutions import Command


def generate_launch_description():

    pkg_robot = get_package_share_directory('robot_3r_description')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    urdf_path = os.path.join(pkg_robot, 'urdf', 'robot_3r.urdf')

    robot_description = Command([
        'xacro ',
        urdf_path
    ])

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            # Sin "-r" para que Gazebo abra pausado
            'gz_args': 'empty.sdf'
        }.items()
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {
                'robot_description': robot_description
            }
        ]
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        name='spawn_robot_3r',
        output='screen',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'robot_3r',
            '-allow_renaming', 'true',
            '-x', '0',
            '-y', '0',
            '-z', '0.05'
        ]
    )

    return LaunchDescription([
        SetEnvironmentVariable(
            name='GZ_SIM_RESOURCE_PATH',
            value=pkg_robot
        ),

        gazebo,
        robot_state_publisher,
        spawn_robot
    ])
