count = 1
tick = 0
function Think()

	local bot = GetBot();
	local loc = bot:GetLocation();
	local loc = tostring(loc);
	local loc = loc:gsub(" ", ";")

	local mana = tostring(bot:GetMana());
	local maxMana = tostring(bot:GetMaxMana());
	local hp = tostring(bot:GetHealth());
	local maxHp = tostring(bot:GetMaxHealth());
	local queuedActions = tostring(bot:NumQueuedActions())
	local neutrals_str = ""
	local lane_creeps_str = ""
	local heroes_str = ""
	local buildings_str = ""

	local nearby_neutral_creeps = bot:GetNearbyNeutralCreeps(1600)
	for _, unit in pairs(nearby_neutral_creeps) do
		neutrals_str = neutrals_str .. "[ " .. tostring(unit) .. " " .. 
		unit:GetUnitName() .. " " .. --name
		unit:GetHealth() .. " " .. --HP 
		unit:GetMaxHealth() .. " " .. --MaxHP
		unit:GetMana() .. " " .. --Mana
		unit:GetMaxMana() .. " " .. --MaxMana
		unit:GetAttackDamage() .. " " .. --AttackDamage with bonuses
		unit:GetArmor() .. " " .. --Armor
		GetUnitToUnitDistance(unit, bot) .. "] " --Distance
    end
    
    local nearby_lane_creeps = bot:GetNearbyLaneCreeps(1600, true)
	for _, unit in pairs(nearby_lane_creeps) do
		lane_creeps_str = lane_creeps_str .. "[ " .. tostring(unit) .. " " .. 
		unit:GetUnitName() .. " " .. --name
		unit:GetHealth() .. " " .. --HP 
		unit:GetMaxHealth() .. " " .. --MaxHP
		unit:GetMana() .. " " .. --Mana
		unit:GetMaxMana() .. " " .. --MaxMana
		unit:GetAttackDamage() .. " " .. --AttackDamage with bonuses
		unit:GetArmor() .. " " .. --Armor
		GetUnitToUnitDistance(unit, bot) .. "] " --Distance
    end

	local enemy_heroes = GetUnitList(UNIT_LIST_ENEMY_HEROES)
    for _, unit in pairs(enemy_heroes) do
		heroes_str = heroes_str .. "[ " .. tostring(unit) .. " " .. 
		unit:GetUnitName() .. " " .. --name
		unit:GetHealth() .. " " .. --HP 
		unit:GetMaxHealth() .. " " .. --MaxHP
		unit:GetMana() .. " " .. --Mana
		unit:GetMaxMana() .. " " .. --MaxMana
		unit:GetAttackDamage() .. " " .. --AttackDamage with bonuses
		unit:GetArmor() .. " " .. --Armor
		GetUnitToUnitDistance(unit, bot) .. "] " --Distance
    end
    
    local enemy_buildings = GetUnitList(UNIT_LIST_ENEMY_BUILDINGS)
    for _, unit in pairs(enemy_buildings) do
		if unit:GetUnitName() == "npc_dota_goodguys_tower1_mid" then
			buildings_str = buildings_str .. "[ " .. tostring(unit) .. " " .. 
			unit:GetUnitName() .. " " .. --name
			unit:GetHealth() .. " " .. --HP 
			unit:GetMaxHealth() .. " " .. --MaxHP
			unit:GetMana() .. " " .. --Mana
			unit:GetMaxMana() .. " " .. --MaxMana
			unit:GetAttackDamage() .. " " .. --AttackDamage with bonuses
			unit:GetArmor() .. " " .. --Armor
			GetUnitToUnitDistance(unit, bot) .. "] " --Distance
		end
    end
    
	local state = ";" .. loc ..
		";" .. hp ..
		";" .. maxHp ..
		";" .. mana ..
		";" .. maxMana ..
		";" .. DotaTime() ..
		";" .. queuedActions ..
		";" .. "[" .. neutrals_str .. "]" ..
		";" .. GetTimeOfDay() ..
		";" .. "[" .. lane_creeps_str .. "]" ..
		";" .. "[" .. heroes_str .. "]" ..
		";" .. "[" .. buildings_str .. "]" ..
		";" .. tick ..
		";" .. GetGameState()

	print(state)
	tick = tick +1;

	local cmd = loadfile(GetScriptDirectory()..'/tmp/'..count);
	if cmd == nil then
		return		
	end

	if string.startswith(cmd(), "Action_MoveDirectly") then
		cmd_split = split(cmd());
		x = tonumber(cmd_split[2]);
		y = tonumber(cmd_split[3]);

		bot:Action_MoveDirectly(Vector(x, y, 0.0));
				
	elseif string.startswith(cmd(), "ActionPush_MoveDirectly") then
		cmd_split = split(cmd());
		x = tonumber(cmd_split[2]);
		y = tonumber(cmd_split[3]);

		bot:ActionPush_MoveDirectly(Vector(x, y, 0.0));
		
	elseif string.startswith(cmd(), "ActionQueue_MoveDirectly") then
		cmd_split = split(cmd());
		x = tonumber(cmd_split[2]);
		y = tonumber(cmd_split[3]);
		print("Queued move to (" .. x .. ", " .. y .. "). Cmd received at tick " .. tick-1 .. ".")

		bot:ActionQueue_MoveDirectly(Vector(x, y, 0.0));
		
	elseif string.startswith(cmd(), "Action_AttackUnit") then
		cmd_split = split(cmd());
		handle = cmd_split[2] .. " " .. cmd_split[3];
		once = cmd_split[4];
		for _, unit in pairs(nearby_neutral_creeps) do
			if tostring(handle) == tostring(unit) then
				if once == "True" then
					bot:Action_AttackUnit(unit, true);
				elseif once == "False" then
					bot:Action_AttackUnit(unit, false);
				end
			end
		end

	elseif string.startswith(cmd(), "ActionPush_AttackUnit") then
		cmd_split = split(cmd());
		handle = cmd_split[2] .. " " .. cmd_split[3];
		once = cmd_split[4];
		for _, unit in pairs(nearby_neutral_creeps) do
			if tostring(handle) == tostring(unit) then
				if once == "True" then
					bot:ActionPush_AttackUnit(unit, true);
				elseif once == "False" then
					bot:ActionPush_AttackUnit(unit, false);
				end
			end
		end
		

	elseif string.startswith(cmd(), "ActionQueue_AttackUnit") then
		cmd_split = split(cmd());
		handle = cmd_split[2] .. " " .. cmd_split[3];
		once = cmd_split[4];
		for _, unit in pairs(nearby_neutral_creeps) do
			if tostring(handle) == tostring(unit) then
				if once == "True" then
					bot:ActionQueue_AttackUnit(unit, true);
					print("Queued attacking unit once. Cmd received at tick " .. tick-1 .. ".")
				elseif once == "False" then
					bot:ActionQueue_AttackUnit(unit, false);
				end
			end
		end

	elseif string.startswith(cmd(), "Action_ClearActions") then
		cmd_split = split(cmd());
		stop = cmd_split[2]
		if stop == "True" then
			bot:Action_ClearActions(true);
		elseif stop == "False" then
			bot:Action_ClearActions(false);
		end
	
	elseif string.startswith(cmd(), "Action_Delay") then
		cmd_split = split(cmd());
		delay = tonumber(cmd_split[2])
		bot:Action_Delay(delay)
	
	elseif string.startswith(cmd(), "ActionPush_Delay") then
		cmd_split = split(cmd());
		delay = tonumber(cmd_split[2])
		bot:ActionPush_Delay(delay)
	
	elseif string.startswith(cmd(), "ActionQueue_Delay") then
		cmd_split = split(cmd());
		delay = tonumber(cmd_split[2])
		bot:ActionQueue_Delay(delay)
		
	elseif cmd() == 'hello' then
		print("Hi there");
		
	else
		print("");
	end

	count = count + 1;


end


function string.startswith(String,Start)
	return string.sub(String,1,string.len(Start))==Start
end


function split(s, pattern, maxsplit)
	local pattern = pattern or ' '
	local maxsplit = maxsplit or -1
	local s = s
	local t = {}
	local patsz = #pattern
	while maxsplit ~= 0 do
		local curpos = 1
		local found = string.find(s, pattern)
		if found ~= nil then
			table.insert(t, string.sub(s, curpos, found - 1))
			curpos = found + patsz
			s = string.sub(s, curpos)
		else
			table.insert(t, string.sub(s, curpos))
			break
		end
		maxsplit = maxsplit - 1
		if maxsplit == 0 then
			table.insert(t, string.sub(s, curpos - patsz - 1))
		end
	end
	return t
end
