/*
 * Copyright (C) 2012 Open Source Robotics Foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
*/
#ifndef GAZEBO_PLUGINS_CAMERABBOXPLUGIN_HH_
#define GAZEBO_PLUGINS_CAMERABBOXPLUGIN_HH_

#include <string>

#include "gazebo/common/Plugin.hh"
#include "gazebo/sensors/CameraSensor.hh"
#include "gazebo/rendering/Camera.hh"
#include "gazebo/util/system.hh"
#include "gazebo/rendering/Scene.hh"
#include "gazebo/common/Events.hh"
namespace gazebo
{
  class CameraBboxPluginPrivate;
  class GAZEBO_VISIBLE CameraBboxPlugin : public SensorPlugin
  {
    public: CameraBboxPlugin();

    /// \brief Destructor
    public: virtual ~CameraBboxPlugin();
    public: virtual void Load(sensors::SensorPtr _sensor, sdf::ElementPtr _sdf);

    public: virtual void OnNewFrame(const unsigned char *_image,
                              unsigned int _width, unsigned int _height,
                              unsigned int _depth, const std::string &_format);

    protected: unsigned int width, height, depth;
    protected: std::string format;

    protected: sensors::CameraSensorPtr parentSensor;
    protected: rendering::CameraPtr camera;
    public: void Update();
    private: event::ConnectionPtr newFrameConnection;
    protected: std::vector<event::ConnectionPtr> connections;

  };
}
#endif
